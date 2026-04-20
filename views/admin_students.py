"""
admin_students.py
-----------------
AdminStudentsView — the Students section of the Admin dashboard.

Displays all registered students in a searchable, sortable table.
Search uses linear_search (O(n), partial match).
Sorting uses merge_sort_students (O(n log n), stable).
Also allows the admin to add new student accounts directly.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from registrar.models import Student
from dsa_lib.merge_sort    import merge_sort_students
from dsa_lib.linear_search import linear_search
from views.theme import (
    FONT_FAMILY, FONT_SMALL,
    BG_SURFACE,
    ACCENT, SUCCESS, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM,
    TREEVIEW_BG, TREEVIEW_ALT,
)


class AdminStudentsView(ttk.Frame):
    """
    Ttk frame that renders the Students admin panel.

    Parameters
    ----------
    parent : tk widget — container provided by AdminDashboard
    app    : UniversityApp — access to app.uni and app._set_status()
    """

    def __init__(self, parent, app):
        super().__init__(parent, style="TFrame")
        self.app = app
        self.uni = app.uni
        self._build()

    # BUILD

    def _build(self):
        # Section header
        hdr = ttk.Frame(self, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=16)
        ttk.Label(hdr_inner, text="Students",
                  font=(FONT_FAMILY, 16, "bold"), foreground=TEXT_PRIMARY,
                  style="Surface.TLabel").pack(side="left")

        sort_frame = ttk.Frame(hdr_inner, style="Surface.TFrame")
        sort_frame.pack(side="right")
        ttk.Button(sort_frame, text="Sort by GPA ↓", style="Accent.TButton",
                   command=lambda: self._sort("gpa")).pack(side="left", padx=4)
        ttk.Button(sort_frame, text="Sort by Name ↑", style="TButton",
                   command=lambda: self._sort("name")).pack(side="left", padx=4)
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        # Search bar
        search_bar = ttk.Frame(self, style="Surface.TFrame")
        search_bar.pack(fill="x", padx=20, pady=12)
        ttk.Label(search_bar, text="🔍", font=(FONT_FAMILY, 11),
                  style="Surface.TLabel").pack(side="left", padx=(0, 6))
        self._search_entry = ttk.Entry(search_bar, width=30, font=(FONT_FAMILY, 10))
        self._search_entry.pack(side="left")
        self._search_entry.bind("<KeyRelease>", lambda e: self.refresh())

        # Add-student form
        card = ttk.Frame(self, style="Surface.TFrame")
        card.pack(fill="x", padx=20, pady=(0, 12))
        ttk.Label(card, text="Add Student", font=(FONT_FAMILY, 10, "bold"),
                  foreground=ACCENT, style="Surface.TLabel").pack(anchor="w", pady=(0, 6))
        fields = ttk.Frame(card, style="Surface.TFrame")
        fields.pack(fill="x")
        for i, lbl in enumerate(["First Name", "Last Name", "Username", "DOB (YYYY-MM-DD)"]):
            ttk.Label(fields, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel"
                      ).grid(row=0, column=i, padx=5, sticky="w")
        self._first = ttk.Entry(fields, width=13)
        self._last  = ttk.Entry(fields, width=13)
        self._user  = ttk.Entry(fields, width=12)
        self._dob   = ttk.Entry(fields, width=13)
        for i, e in enumerate([self._first, self._last, self._user, self._dob]):
            e.grid(row=1, column=i, padx=5, pady=(4, 0), sticky="ew")
        ttk.Button(fields, text="➕ Add", style="Success.TButton",
                   command=self._add_student).grid(row=1, column=4, padx=(12, 0))

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20)

        # Students treeview
        tree_wrap = ttk.Frame(self, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("username", "name", "gpa", "completed", "active")
        self._tree = ttk.Treeview(tree_wrap, columns=cols,
                                  show="headings", selectmode="browse")
        for col, heading, w, anchor in [
            ("username",  "Username",      100, "center"),
            ("name",      "Full Name",     190, "w"),
            ("gpa",       "GPA",            65, "center"),
            ("completed", "Completed",      85, "center"),
            ("active",    "Active Courses",  0, "w"),
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=w, anchor=anchor, stretch=(col == "active"))

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.refresh()

    # ACTIONS

    def _add_student(self):
        first = self._first.get().strip()
        last  = self._last.get().strip()
        user  = self._user.get().strip()
        dob   = self._dob.get().strip()
        if not all([first, last, user, dob]):
            messagebox.showwarning("Validation", "All fields are required.")
            return
        if user in self.uni.students:
            messagebox.showwarning("Duplicate", f"Username '{user}' already exists.")
            return
        self.uni.students[user] = Student(first, last, user, dob)
        self.uni._save()
        self.refresh()
        self.app._refresh_header_stats()
        self.app._set_status(f"Student '{first} {last}' added.")
        for e in [self._first, self._last, self._user, self._dob]:
            e.delete(0, "end")

    def _sort(self, by):
        """Sort the student list and repopulate the tree."""
        students = list(self.uni.students.values())
        if by == "gpa":
            sorted_list = merge_sort_students(
                students, key_func=lambda s: s.gpa, reverse=True)
            self.app._set_status(
                "Students sorted by GPA (descending).")
        else:
            sorted_list = merge_sort_students(
                students, key_func=lambda s: s.last.lower(), reverse=False)
            self.app._set_status(
                "Students sorted by last name (ascending).")
        self._populate_tree(sorted_list)

    # REFRESH

    def refresh(self):
        """
        Re-filter with the current search query (linear_search) and
        repopulate the treeview.
        """
        query = self._search_entry.get().strip() if hasattr(self, "_search_entry") else ""
        if query:
            results = linear_search(
                list(self.uni.students.values()),
                query,
                key_func=lambda s: f"{s.first} {s.last} {s.username}",
            )
            self.app._set_status(f"{len(results)} match(es) found for '{query}'.")
        else:
            results = list(self.uni.students.values())
        self._populate_tree(results)

    def _populate_tree(self, students):
        for item in self._tree.get_children():
            self._tree.delete(item)
        for i, s in enumerate(students):
            tag = "even" if i % 2 == 0 else "odd"
            active = ", ".join(s.active_schedule) if s.active_schedule else "—"
            self._tree.insert("", "end", values=(
                s.username, s.full_name,
                f"{s.gpa:.2f}", len(s.completed_courses), active,
            ), tags=(tag,))
        self._tree.tag_configure("even", background=TREEVIEW_BG)
        self._tree.tag_configure("odd",  background=TREEVIEW_ALT)
