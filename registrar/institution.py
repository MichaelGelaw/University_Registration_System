"""
institution.py
--------------
The Institution class — the top-level object that owns the course catalog
(CourseBST), student and admin registries, and all course offerings.

Responsibilities
----------------
- Registration pipeline   (prereq + conflict checks → enroll or waitlist)
- Drop logic              (remove student + FCFS promotion from LinkedQueue)
- Grade finalization      (active → completed, GPA recalculation)
- Student search          (linear_search by name / username)
- JSON persistence        (save / load the full institutional state)
"""

import json
import os

from dsa_lib.course_bst  import CourseBST
from dsa_lib.linear_search import linear_search
from .models import (
    Course, CourseOffering, Student, Admin,
    GPA_SCALE, hash_password,
)

DATA_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "university_data.json")
SAMPLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "university_data.sample.json")


class Institution:
    """
    Top-level object managing the BST catalog, students, admins, and offerings.

    All mutation methods call _save() automatically so the JSON file is
    always in sync with in-memory state.
    """

    def __init__(self, name):
        self.name      = name
        self.catalog   = CourseBST()
        self.students  = {}     # {username: Student}
        self.admins    = {}     # {username: Admin}
        self.offerings = []     # list[CourseOffering]

    # ── Search ────────────────────────────────────────────────────────

    def search_students(self, query):
        """Linear search across first name, last name, and username."""
        all_students = list(self.students.values())
        return linear_search(
            all_students,
            query,
            key_func=lambda s: f"{s.first} {s.last} {s.username}",
        )

    def find_offering(self, course_name, section=None):
        """Find an offering by course name and optionally section number."""
        for o in self.offerings:
            if o.course.name.lower() == course_name.lower():
                if section is None or o.section == section:
                    return o
        return None

    def get_offerings_for_course(self, course_name):
        """Return all offerings for a given course name."""
        return [o for o in self.offerings if o.course.name.lower() == course_name.lower()]

    def check_time_conflict(self, student_username, new_offering):
        """
        Return True if the student already has a course at the same time slot.
        Resolved here at the Institution level because only Institution has
        access to all current offerings.
        """
        student = self.students.get(student_username)
        if not student:
            return False
        for offering_name in student.active_schedule:
            for o in self.offerings:
                if o.display_name == offering_name and o.time_slot == new_offering.time_slot:
                    return True
        return False

    # ── Registration pipeline ─────────────────────────────────────────

    def register_student(self, student_username, offering):
        """
        Full registration pipeline:
          1. Validate student exists
          2. Check for time conflicts (Institution level)
          3. Delegate to offering.register_request (prereqs + capacity)
          4. Persist
        """
        student = self.students.get(student_username)
        if not student:
            return "Student not found."

        if self.check_time_conflict(student_username, offering):
            return f"TIME CONFLICT: {offering.time_slot} overlaps with an existing course."

        result = offering.register_request(student)
        self._save()
        return result

    def drop_student(self, student_username, offering):
        """Drop a student and auto-promote the next from the FCFS waitlist."""
        student = self.students.get(student_username)
        if student and offering.display_name in student.active_schedule:
            student.active_schedule.remove(offering.display_name)

        # Peek at who will be promoted before the drop
        promoted = offering.waitlist.peek() if not offering.waitlist.is_empty() else None

        result = offering.drop_student(student_username)

        # Add the offering to the promoted student's active schedule
        if promoted and promoted in self.students:
            promoted_student = self.students[promoted]
            if offering.display_name not in promoted_student.active_schedule:
                promoted_student.active_schedule.append(offering.display_name)

        self._save()
        return result

    def finalize_grade(self, student_username, offering, grade):
        """
        Assign a grade, move the course from active → completed,
        and recalculate the student's GPA.
        """
        result = offering.assign_grade(student_username, grade)
        if result.startswith("Grade"):
            student = self.students.get(student_username)
            if student:
                student.completed_courses[offering.course.name] = grade
                if offering.display_name in student.active_schedule:
                    student.active_schedule.remove(offering.display_name)
            self._save()
        return result

    # ── Persistence ───────────────────────────────────────────────────

    def _save(self):
        """Auto-save current state to the default JSON file."""
        self.save(DATA_FILE)

    def save(self, filepath=None):
        """Serialize the full institution state to JSON."""
        if filepath is None:
            filepath = DATA_FILE

        data = {
            "institution_name": self.name,
            "courses":   [c.to_dict() for c in self.catalog.inorder()],
            "students":  {u: s.to_dict() for u, s in self.students.items()},
            "admins":    {u: a.to_dict() for u, a in self.admins.items()},
            "offerings": [o.to_dict() for o in self.offerings],
        }

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, filepath=None):
        """
        Rehydrate an Institution from JSON.

        On first run (no university_data.json), seeds from
        university_data.sample.json so the app starts with demo data.
        Rebuilds the CourseBST, Student dict, and LinkedQueue waitlists
        from the flat JSON representation.
        """
        if filepath is None:
            filepath = DATA_FILE

        if not os.path.exists(filepath):
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

        # 1. Rebuild BST from catalog list
        for c_data in data.get("courses", []):
            inst.catalog.insert(Course.from_dict(c_data))

        # 2. Rebuild students
        for username, s_data in data.get("students", {}).items():
            inst.students[username] = Student.from_dict(s_data)

        # 3. Rebuild admins (provision a default admin if none exist)
        admins_data = data.get("admins", {})
        if not admins_data:
            default = Admin("System", "Admin", "admin", "admin@university.edu",
                            hash_password("password123"), "")
            admins_data["admin"] = default.to_dict()

        for username, a_data in admins_data.items():
            inst.admins[username] = Admin.from_dict(a_data)

        # 4. Rebuild offerings — re-link to BST courses, re-enqueue waitlists
        for o_data in data.get("offerings", []):
            course = inst.catalog.search(o_data["course_name"])
            if course is None:
                continue  # skip offerings whose course was deleted

            offering = CourseOffering(
                course    = course,
                section   = o_data.get("section",   1),
                year      = o_data.get("year",       2026),
                quarter   = o_data.get("quarter",    "Spring"),
                capacity  = o_data.get("capacity",   30),
                time_slot = o_data.get("time_slot",  "MW 10:00-11:30"),
            )
            offering.enrolled_students = o_data.get("enrolled_students", [])
            offering.grades            = o_data.get("grades",            {})

            # Restore FCFS waitlist order from the JSON array
            for username in o_data.get("waitlist", []):
                offering.waitlist.enqueue(username)

            inst.offerings.append(offering)

        return inst
