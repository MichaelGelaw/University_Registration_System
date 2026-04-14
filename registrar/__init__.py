"""
registrar — University data models and business logic
=====================================================
Re-exports every public name so all existing import statements
(``from registrar import Institution``, etc.) keep working unchanged.

Module breakdown
----------------
models.py      — GPA_SCALE, hash_password, Course, CourseOffering, Student, Admin
institution.py — Institution  (catalog BST, registration, persistence)
"""

from .models import (
    GPA_SCALE,
    hash_password,
    Course,
    CourseOffering,
    Student,
    Admin,
)
from .institution import Institution

__all__ = [
    "GPA_SCALE",
    "hash_password",
    "Course",
    "CourseOffering",
    "Student",
    "Admin",
    "Institution",
]
