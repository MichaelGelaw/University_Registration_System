"""
admin_grades.py
---------------
AdminGradesView — the Grades & Enrollment section of the Admin dashboard.

Allows the admin to:
  - Select a course offering and assign a letter grade to an enrolled student
    (which moves the course from active → completed and recalculates GPA).
  - Drop a student from an offering, triggering automatic promotion of the
    next student from the FCFS LinkedQueue waitlist.

Cross-view side effects after mutations:
  - Students view is refreshed (GPA column changes).
  - Offerings view is refreshed (enrollment/waitlist counts change).
"""

import tkinter as tk
from tkinter import ttk, messagebox

from views.theme import (
    FONT_FAMILY, FONT_SMALL,
    BG_SURFACE,
    ACCENT, SUCCESS, DANGER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM,
    TREEVIEW_BG, TREEVIEW_ALT,
)


class AdminGradesView(ttk.Frame):
    """
    Ttk frame that renders the Grades & Enrollment admin panel.

    Parameters
    ----------
    parent : tk widget — container provided by AdminDashboard
    app    : UniversityApp — access to app.uni, app._set_status(),
             and sibling views via app.admin_dashboard.*
    """

    def __init__(self, parent, app):
        super().__init__(parent, style="TFrame")
        self.app = app
        self.uni = app.uni
        self._build()

    # ── Build ─────────────────────────────────────────────────────────

    def _build(self):
        offering_names = [
            f"{o.display_name} ({o.quarter} {o.year})" for o in self.uni.offerings
        ]

        # Section header
        hdr = ttk.Frame(self, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=16)
        ttk.Label(hdr_inner, text="Grades & Enrollment",
                  font=(FONT_FAMILY, 16, "bold"), foreground=TEXT_PRIMARY,
                  style="Surface.TLabel").pack(side="left")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        # Two-column control area
        controls = ttk.Frame(self, style="Surface.TFrame")
        controls.pack(fill="x", padx=20, pady=16)
        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)

        # ── Assign grade (left card) ──────────────────────────────────
        gc = ttk.Frame(controls, style="Surface.TFrame")
        gc.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ttk.Label(gc, text="Assign Grade", font=(FONT_FAMILY, 10, "bold"),
                  foreground=ACCENT, style="Surface.TLabel"
                  ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))
        for i, lbl in enumerate(["Offering", "Student", "Grade"]):
            ttk.Label(gc, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel"
                      ).grid(row=1, column=i, padx=5, sticky="w")

        self._grade_offering = ttk.Combobox(gc, values=offering_names,
                                            width=22, state="readonly")
        self._grade_offering.grid(row=2, column=0, padx=5, pady=(4, 0), sticky="ew")
        self._grade_offering.bind("<<ComboboxSelected>>", self._on_grade_offering_change)

        self._grade_student = ttk.Combobox(gc, width=14, state="readonly")
        self._grade_student.grid(row=2, column=1, padx=5, pady=(4, 0))

        self._grade_value = ttk.Combobox(
            gc, values=["A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-","F"],
            width=5, state="readonly")
        self._grade_value.grid(row=2, column=2, padx=5, pady=(4, 0))

        ttk.Button(gc, text="✅ Assign", style="Success.TButton",
                   command=self._assign_grade
                   ).grid(row=2, column=3, padx=(10, 0), pady=(4, 0))

        # ── Drop student (right card) ─────────────────────────────────
        dc = ttk.Frame(controls, style="Surface.TFrame")
        dc.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ttk.Label(dc, text="Drop Student", font=(FONT_FAMILY, 10, "bold"),
                  foreground=DANGER, style="Surface.TLabel"
                  ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))
        for i, lbl in enumerate(["Offering", "Student"]):
            ttk.Label(dc, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel"
                      ).grid(row=1, column=i, padx=5, sticky="w")

        self._drop_offering = ttk.Combobox(dc, values=offering_names,
                                           width=22, state="readonly")
        self._drop_offering.grid(row=2, column=0, padx=5, pady=(4, 0), sticky="ew")
        self._drop_offering.bind("<<ComboboxSelected>>", self._on_drop_offering_change)

        self._drop_student = ttk.Combobox(dc, width=14, state="readonly")
        self._drop_student.grid(row=2, column=1, padx=5, pady=(4, 0))

        ttk.Button(dc, text="🚫 Drop", style="Danger.TButton",
                   command=self._drop_student_action
                   ).grid(row=2, column=2, padx=(10, 0), pady=(4, 0))

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=(4, 0))

        # ── Enrollment detail tree ────────────────────────────────────
        lbl_row = ttk.Frame(self, style="TFrame")
        lbl_row.pack(fill="x", padx=24, pady=(12, 4))
        ttk.Label(lbl_row, text="Enrollment Details",
                  font=(FONT_FAMILY, 10, "bold"), foreground=TEXT_PRIMARY).pack(side="left")

        tree_wrap = ttk.Frame(self, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        cols = ("student", "status", "grade")
        self._enroll_tree = ttk.Treeview(tree_wrap, columns=cols, show="headings")
        for col, heading, w in [
            ("student", "Student", 200),
            ("status",  "Status",  130),
            ("grade",   "Grade",    80),
        ]:
            self._enroll_tree.heading(col, text=heading)
            self._enroll_tree.column(col, width=w, anchor="center")

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical",
                            command=self._enroll_tree.yview)
        self._enroll_tree.configure(yscrollcommand=vsb.set)
        self._enroll_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    # ── Combobox callbacks ────────────────────────────────────────────

    def _on_grade_offering_change(self, event=None):
        idx = self._grade_offering.current()
        if idx < 0 or idx >= len(self.uni.offerings):
            return
        offering = self.uni.offerings[idx]
        self._grade_student.config(values=offering.enrolled_students)
        self._refresh_enroll_tree(offering)

    def _on_drop_offering_change(self, event=None):
        idx = self._drop_offering.current()
        if idx < 0 or idx >= len(self.uni.offerings):
            return
        offering = self.uni.offerings[idx]
        self._drop_student.config(values=offering.enrolled_students)
        self._refresh_enroll_tree(offering)

    # ── Actions ───────────────────────────────────────────────────────

    def _assign_grade(self):
        idx     = self._grade_offering.current()
        student = self._grade_student.get()
        grade   = self._grade_value.get()
        if idx < 0 or not student or not grade:
            messagebox.showwarning("Validation", "Select offering, student, and grade.")
            return
        offering = self.uni.offerings[idx]
        result   = self.uni.finalize_grade(student, offering, grade)
        messagebox.showinfo("Grade Entry", result)
        self._refresh_enroll_tree(offering)
        # Refresh sibling views — student GPA may have changed
        self.app.admin_dashboard.students_view.refresh()
        self.app._set_status(result)

    def _drop_student_action(self):
        idx     = self._drop_offering.current()
        student = self._drop_student.get()
        if idx < 0 or not student:
            messagebox.showwarning("Validation", "Select offering and student.")
            return
        offering = self.uni.offerings[idx]
        result   = self.uni.drop_student(student, offering)
        messagebox.showinfo("Drop Student", result)
        # Refresh the two comboboxes and the enroll tree
        self._on_drop_offering_change()
        self._on_grade_offering_change()
        # Refresh sibling views — enrollment counts and schedule changed
        self.app.admin_dashboard.students_view.refresh()
        self.app.admin_dashboard.offerings_view.refresh()
        self.app._set_status(result)

    # ── Refresh ───────────────────────────────────────────────────────

    def _refresh_enroll_tree(self, offering):
        """Rebuild the enrollment detail table for the given offering."""
        for item in self._enroll_tree.get_children():
            self._enroll_tree.delete(item)
        for i, u in enumerate(offering.enrolled_students):
            grade = offering.grades.get(u, "—")
            tag   = "even" if i % 2 == 0 else "odd"
            self._enroll_tree.insert("", "end", values=(u, "Enrolled", grade), tags=(tag,))
        for i, u in enumerate(offering.waitlist.to_list()):
            self._enroll_tree.insert("", "end",
                                     values=(u, f"Waitlist #{i+1}", "—"),
                                     tags=("waitlist",))
        self._enroll_tree.tag_configure("even",     background=TREEVIEW_BG)
        self._enroll_tree.tag_configure("odd",      background=TREEVIEW_ALT)
        self._enroll_tree.tag_configure("waitlist", background="#fef3c7",
                                        foreground="#92400e")

    def refresh(self):
        """
        Called when the panel is navigated to. Refreshes the offering
        combobox values in case new offerings were created since last visit.
        """
        offering_names = [
            f"{o.display_name} ({o.quarter} {o.year})" for o in self.uni.offerings
        ]
        self._grade_offering.config(values=offering_names)
        self._drop_offering.config(values=offering_names)
