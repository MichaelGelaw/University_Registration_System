import json
import os
from dsa_lib.structures import LinkedQueue, CourseBST
from dsa_lib.sorting import linear_search
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ── Grade → quality-point mapping (single source of truth) ──────────
# Imported by app.py as well — update here only.
GPA_SCALE = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F":  0.0,
}

DATA_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "university_data.json")
SAMPLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "university_data.sample.json")



class Course:
    """A course in the university catalog (stored in the BST)."""

    def __init__(self, dept, number, name, credits, prereqs=None):
        self.dept = dept
        self.number = number
        self.name = name
        self.credits = credits
        self.prereqs = prereqs if prereqs else []

    def to_dict(self):
        return {
            "dept": self.dept,
            "number": self.number,
            "name": self.name,
            "credits": self.credits,
            "prereqs": self.prereqs,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["dept"], d["number"], d["name"], d["credits"], d.get("prereqs", []))

    def __repr__(self):
        return f"{self.dept} {self.number}: {self.name}"


class CourseOffering:
    """A specific section of a course offered in a given year/quarter."""

    def __init__(self, course, section, year, quarter, capacity=30, time_slot="MW 10:00-11:30"):
        self.course = course
        self.section = section
        self.year = year
        self.quarter = quarter
        self.capacity = capacity
        self.time_slot = time_slot
        self.enrolled_students = []
        self.waitlist = LinkedQueue()
        self.grades = {}

    @property
    def seats_available(self):
        return self.capacity - len(self.enrolled_students)

    @property
    def is_full(self):
        return len(self.enrolled_students) >= self.capacity

    @property
    def display_name(self):
        return f"{self.course.dept} {self.course.number}-{self.section}"

    def register_request(self, student):
        """Main enrollment logic: prereqs → conflicts → capacity → enqueue."""
        # Already enrolled?
        if student.username in self.enrolled_students:
            return "Already enrolled in this course."

        # Already on waitlist?
        if student.username in self.waitlist:
            pos = self.waitlist.position_of(student.username)
            return f"Already on waitlist (position #{pos})."

        # 1. Prerequisite Check
        for pre in self.course.prereqs:
            if pre not in student.completed_courses:
                return f"Missing prerequisite: {pre}"

        # 2. Schedule Conflict Check — handled at Institution.check_time_conflict(),
        #    which is called by Institution.register_student() before this method.

        # 3. Capacity Check → Enroll or Queue
        if not self.is_full:
            self.enrolled_students.append(student.username)
            student.active_schedule.append(self.display_name)
            return "SUCCESS: Enrolled!"
        else:
            self.waitlist.enqueue(student.username)
            pos = self.waitlist.position_of(student.username)
            return f"WAITLIST: Course full — added to waitlist (position #{pos})."

    def drop_student(self, student_username):
        """Removes a student and promotes the next from the FCFS Queue."""
        if student_username not in self.enrolled_students:
            return "Student not found in this offering."

        self.enrolled_students.remove(student_username)
        # Remove the grade if any
        self.grades.pop(student_username, None)

        # FCFS Promotion
        if not self.waitlist.is_empty():
            next_student = self.waitlist.dequeue()
            self.enrolled_students.append(next_student)
            return f"Dropped {student_username}. {next_student} promoted from waitlist!"
        return f"Dropped {student_username}. Seat is now vacant."

    def assign_grade(self, student_username, grade):
        """Assign a letter grade to an enrolled student."""
        if student_username not in self.enrolled_students:
            return "Student not enrolled in this course."
        valid_grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]
        if grade not in valid_grades:
            return f"Invalid grade. Must be one of: {', '.join(valid_grades)}"
        self.grades[student_username] = grade
        return f"Grade {grade} assigned to {student_username}."

    def to_dict(self):
        return {
            "course_name": self.course.name,
            "section": self.section,
            "year": self.year,
            "quarter": self.quarter,
            "capacity": self.capacity,
            "time_slot": self.time_slot,
            "enrolled_students": self.enrolled_students,
            "waitlist": self.waitlist.to_list(),
            "grades": self.grades,
        }

    def __repr__(self):
        return f"{self.display_name} ({self.quarter} {self.year})"


class Student:
    """A student enrolled at the university."""

    def __init__(self, first, last, username, dob, email="", password_hash="", avatar_path=""):
        self.first = first
        self.last = last
        self.username = username
        self.dob = dob
        self.email = email
        self.password_hash = password_hash
        self.avatar_path = avatar_path
        self.active_schedule = []          # List of offering display names (strings)
        self.completed_courses = {}        # {course_name: grade}

    @property
    def gpa(self):
        grades = [GPA_SCALE.get(g, 0.0) for g in self.completed_courses.values()]
        return round(sum(grades) / len(grades), 2) if grades else 0.0

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

    def to_dict(self):
        return {
            "first": self.first,
            "last": self.last,
            "username": self.username,
            "dob": self.dob,
            "email": self.email,
            "password_hash": self.password_hash,
            "avatar_path": self.avatar_path,
            "completed_courses": self.completed_courses,
            "active_schedule": self.active_schedule,
        }

    @classmethod
    def from_dict(cls, d):
        s = cls(d["first"], d["last"], d["username"], d["dob"], 
                d.get("email", ""), d.get("password_hash", ""), d.get("avatar_path", ""))
        s.completed_courses = d.get("completed_courses", {})
        s.active_schedule = d.get("active_schedule", [])
        return s

    def __repr__(self):
        return f"{self.full_name} (@{self.username}) — GPA: {self.gpa}"


class Admin:
    """An administrator who manages the institution."""

    def __init__(self, first, last, username, email="", password_hash="", avatar_path=""):
        self.first = first
        self.last = last
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.avatar_path = avatar_path
        
    @property
    def full_name(self):
        return f"{self.first} {self.last}"

    def to_dict(self):
        return {
            "first": self.first,
            "last": self.last,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "avatar_path": self.avatar_path,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["first"], d["last"], d["username"], 
                   d.get("email", ""), d.get("password_hash", ""), d.get("avatar_path", ""))
        
    def __repr__(self):
        return f"Admin: {self.full_name} (@{self.username})"


class Institution:
    """Top-level object managing the BST catalog, students, and offerings."""

    def __init__(self, name):
        self.name = name
        self.catalog = CourseBST()
        self.students = {}      # {username: Student}
        self.admins = {}        # {username: Admin}
        self.offerings = []     # List[CourseOffering]

    # ─── Search ──────────────────────────────────────────────

    def search_students(self, query):
        """Uses linear_search from dsa_lib to filter students by partial name match."""
        all_students = list(self.students.values())
        return linear_search(
            all_students,
            query,
            key_func=lambda s: f"{s.first} {s.last} {s.username}",
        )

    def find_offering(self, course_name, section=None):
        """Find an offering by course name (and optionally section)."""
        for o in self.offerings:
            if o.course.name.lower() == course_name.lower():
                if section is None or o.section == section:
                    return o
        return None

    def get_offerings_for_course(self, course_name):
        """Returns all offerings for a given course name."""
        return [o for o in self.offerings if o.course.name.lower() == course_name.lower()]

    def check_time_conflict(self, student_username, new_offering):
        """Check if the student has a time conflict with the new offering."""
        student = self.students.get(student_username)
        if not student:
            return False
        for offering_name in student.active_schedule:
            for o in self.offerings:
                if o.display_name == offering_name and o.time_slot == new_offering.time_slot:
                    return True
        return False

    def register_student(self, student_username, offering):
        """Full registration pipeline: conflict check → offering.register_request."""
        student = self.students.get(student_username)
        if not student:
            return "Student not found."

        # Time conflict check at institution level
        if self.check_time_conflict(student_username, offering):
            return f"TIME CONFLICT: {offering.time_slot} overlaps with an existing course."

        result = offering.register_request(student)
        self._save()
        return result

    def drop_student(self, student_username, offering):
        """Drop a student from an offering and auto-promote waitlist."""
        student = self.students.get(student_username)
        if student and offering.display_name in student.active_schedule:
            student.active_schedule.remove(offering.display_name)

        # If the promoted student exists, add the offering to their schedule
        promoted = None
        if not offering.waitlist.is_empty():
            promoted = offering.waitlist.peek()

        result = offering.drop_student(student_username)

        # Add offering to promoted student's schedule
        if promoted and promoted in self.students:
            promoted_student = self.students[promoted]
            if offering.display_name not in promoted_student.active_schedule:
                promoted_student.active_schedule.append(offering.display_name)

        self._save()
        return result

    def finalize_grade(self, student_username, offering, grade):
        """Assign grade → move from active to completed → update GPA."""
        result = offering.assign_grade(student_username, grade)
        if result.startswith("Grade"):
            student = self.students.get(student_username)
            if student:
                student.completed_courses[offering.course.name] = grade
                if offering.display_name in student.active_schedule:
                    student.active_schedule.remove(offering.display_name)
            self._save()
        return result

    # ─── Persistence ─────────────────────────────────────────

    def _save(self):
        """Auto-save current state to JSON."""
        self.save(DATA_FILE)

    def save(self, filepath=None):
        """Serialize the entire institution to JSON."""
        if filepath is None:
            filepath = DATA_FILE

        data = {
            "institution_name": self.name,
            "courses": [c.to_dict() for c in self.catalog.inorder()],
            "students": {u: s.to_dict() for u, s in self.students.items()},
            "admins": {u: a.to_dict() for u, a in self.admins.items()},
            "offerings": [o.to_dict() for o in self.offerings],
        }

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, filepath=None):
        """Rehydrate Institution from JSON — rebuilds BST, students, and queues.
        
        On first run (no university_data.json), automatically seeds from
        university_data.sample.json so the app starts with showcase data.
        """
        if filepath is None:
            filepath = DATA_FILE

        if not os.path.exists(filepath):
            # Seed from sample if available
            if os.path.exists(SAMPLE_FILE):
                import shutil
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                shutil.copy2(SAMPLE_FILE, filepath)
                print(f"[INFO] Seeded '{filepath}' from sample data.")
            else:
                return cls("Tech University")

        with open(filepath, "r") as f:
            data = json.load(f)

        inst = cls(data.get("institution_name", "Tech University"))

        # 1. Rebuild BST from catalog
        for c_data in data.get("courses", []):
            course = Course.from_dict(c_data)
            inst.catalog.insert(course)

        # 2. Rebuild students
        students_data = data.get("students", {})
        for username, s_data in students_data.items():
            inst.students[username] = Student.from_dict(s_data)

        # 2b. Rebuild admins
        admins_data = data.get("admins", {})
        
        # Provision default admin if no admins exist
        if not admins_data:
            default_admin = Admin("System", "Admin", "admin", "admin@university.edu", hash_password("password123"), "")
            admins_data["admin"] = default_admin.to_dict()
            
        for username, a_data in admins_data.items():
            inst.admins[username] = Admin.from_dict(a_data)

        # 3. Rebuild offerings (re-link to BST courses, re-enqueue waitlists)
        for o_data in data.get("offerings", []):
            course = inst.catalog.search(o_data["course_name"])
            if course is None:
                continue  # Skip orphaned offerings

            offering = CourseOffering(
                course=course,
                section=o_data.get("section", 1),
                year=o_data.get("year", 2026),
                quarter=o_data.get("quarter", "Spring"),
                capacity=o_data.get("capacity", 30),
                time_slot=o_data.get("time_slot", "MW 10:00-11:30"),
            )
            offering.enrolled_students = o_data.get("enrolled_students", [])
            offering.grades = o_data.get("grades", {})

            # Re-enqueue waitlist nodes into the LinkedQueue (preserving FCFS order)
            for username in o_data.get("waitlist", []):
                offering.waitlist.enqueue(username)

            inst.offerings.append(offering)

        return inst