"""Data model classes for courses, offerings, students, and admins."""

import hashlib
from dsa_lib.linked_queue import LinkedQueue


# ── Grade → quality-point mapping ────────────────────────────────────
# Import this constant wherever GPA calculation or transcript display is needed.
GPA_SCALE = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F":  0.0,
}


def hash_password(password):
    """Return the SHA-256 hex digest of the given plaintext password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ─────────────────────────────────────────────────────────────────────
#  Course
# ─────────────────────────────────────────────────────────────────────

class Course:
    """A course in the university catalog (stored in the CourseBST)."""

    def __init__(self, dept, number, name, credits, prereqs=None):
        self.dept    = dept
        self.number  = number
        self.name    = name
        self.credits = credits
        self.prereqs = prereqs if prereqs else []

    def to_dict(self):
        return {
            "dept":    self.dept,
            "number":  self.number,
            "name":    self.name,
            "credits": self.credits,
            "prereqs": self.prereqs,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["dept"], d["number"], d["name"], d["credits"], d.get("prereqs", []))

    def __repr__(self):
        return f"{self.dept} {self.number}: {self.name}"


# ─────────────────────────────────────────────────────────────────────
#  CourseOffering
# ─────────────────────────────────────────────────────────────────────

class CourseOffering:
    """
    A scheduled section of a Course offered in a specific quarter/year.

    Maintains an enrolled_students list and a LinkedQueue waitlist.
    Enrollment follows FCFS: when a seat opens, the first student in the
    queue is automatically promoted.
    """

    def __init__(self, course, section, year, quarter, capacity=30,
                 time_slot="MW 10:00-11:30"):
        self.course   = course
        self.section  = section
        self.year     = year
        self.quarter  = quarter
        self.capacity = capacity
        self.time_slot = time_slot
        self.enrolled_students = []
        self.waitlist = LinkedQueue()
        self.grades   = {}

    # ── Computed properties ───────────────────────────────────────────

    @property
    def seats_available(self):
        return self.capacity - len(self.enrolled_students)

    @property
    def is_full(self):
        return len(self.enrolled_students) >= self.capacity

    @property
    def display_name(self):
        return f"{self.course.dept} {self.course.number}-{self.section}"

    # ── Enrollment logic ──────────────────────────────────────────────

    def register_request(self, student):
        """
        Attempt to enroll a student.

        Pipeline: duplicate check → prerequisite check →
                  schedule-conflict check (Institution level) →
                  capacity check → enroll or enqueue.
        """
        if student.username in self.enrolled_students:
            return "Already enrolled in this course."

        if student.username in self.waitlist:
            pos = self.waitlist.position_of(student.username)
            return f"Already on waitlist (position #{pos})."

        # 1. Prerequisite check
        for pre in self.course.prereqs:
            if pre not in student.completed_courses:
                return f"Missing prerequisite: {pre}"

        # 2. Schedule conflict check — handled at Institution.check_time_conflict(),
        #    which is called by Institution.register_student() before this method.

        # 3. Capacity check → enroll directly or add to FCFS queue
        if not self.is_full:
            self.enrolled_students.append(student.username)
            student.active_schedule.append(self.display_name)
            return "SUCCESS: Enrolled!"
        else:
            self.waitlist.enqueue(student.username)
            pos = self.waitlist.position_of(student.username)
            return f"WAITLIST: Course full — added to waitlist (position #{pos})."

    def drop_student(self, student_username):
        """
        Remove a student and promote the next from the FCFS queue (if any).
        """
        if student_username not in self.enrolled_students:
            return "Student not found in this offering."

        self.enrolled_students.remove(student_username)
        self.grades.pop(student_username, None)

        if not self.waitlist.is_empty():
            next_student = self.waitlist.dequeue()
            self.enrolled_students.append(next_student)
            return f"Dropped {student_username}. {next_student} promoted from waitlist!"
        return f"Dropped {student_username}. Seat is now vacant."

    def assign_grade(self, student_username, grade):
        """Assign a letter grade to an enrolled student."""
        if student_username not in self.enrolled_students:
            return "Student not enrolled in this course."
        valid_grades = list(GPA_SCALE.keys())
        if grade not in valid_grades:
            return f"Invalid grade. Must be one of: {', '.join(valid_grades)}"
        self.grades[student_username] = grade
        return f"Grade {grade} assigned to {student_username}."

    # ── Serialization ─────────────────────────────────────────────────

    def to_dict(self):
        return {
            "course_name":       self.course.name,
            "section":           self.section,
            "year":              self.year,
            "quarter":           self.quarter,
            "capacity":          self.capacity,
            "time_slot":         self.time_slot,
            "enrolled_students": self.enrolled_students,
            "waitlist":          self.waitlist.to_list(),
            "grades":            self.grades,
        }

    def __repr__(self):
        return f"{self.display_name} ({self.quarter} {self.year})"


# ─────────────────────────────────────────────────────────────────────
#  Student
# ─────────────────────────────────────────────────────────────────────

class Student:
    """A student enrolled at the university."""

    def __init__(self, first, last, username, dob,
                 email="", password_hash="", avatar_path=""):
        self.first         = first
        self.last          = last
        self.username      = username
        self.dob           = dob
        self.email         = email
        self.password_hash = password_hash
        self.avatar_path   = avatar_path
        self.active_schedule    = []   # list of offering display_name strings
        self.completed_courses  = {}   # {course_name: grade}

    @property
    def gpa(self):
        grades = [GPA_SCALE.get(g, 0.0) for g in self.completed_courses.values()]
        return round(sum(grades) / len(grades), 2) if grades else 0.0

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

    def to_dict(self):
        return {
            "first":            self.first,
            "last":             self.last,
            "username":         self.username,
            "dob":              self.dob,
            "email":            self.email,
            "password_hash":    self.password_hash,
            "avatar_path":      self.avatar_path,
            "completed_courses": self.completed_courses,
            "active_schedule":  self.active_schedule,
        }

    @classmethod
    def from_dict(cls, d):
        s = cls(
            d["first"], d["last"], d["username"], d["dob"],
            d.get("email", ""), d.get("password_hash", ""), d.get("avatar_path", "")
        )
        s.completed_courses = d.get("completed_courses", {})
        s.active_schedule   = d.get("active_schedule",   [])
        return s

    def __repr__(self):
        return f"{self.full_name} (@{self.username}) — GPA: {self.gpa}"


# ─────────────────────────────────────────────────────────────────────
#  Admin
# ─────────────────────────────────────────────────────────────────────

class Admin:
    """An administrator account."""

    def __init__(self, first, last, username,
                 email="", password_hash="", avatar_path=""):
        self.first         = first
        self.last          = last
        self.username      = username
        self.email         = email
        self.password_hash = password_hash
        self.avatar_path   = avatar_path

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

    def to_dict(self):
        return {
            "first":         self.first,
            "last":          self.last,
            "username":      self.username,
            "email":         self.email,
            "password_hash": self.password_hash,
            "avatar_path":   self.avatar_path,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["first"], d["last"], d["username"],
            d.get("email", ""), d.get("password_hash", ""), d.get("avatar_path", "")
        )

    def __repr__(self):
        return f"Admin: {self.full_name} (@{self.username})"
