"""
admin_offerings.py
------------------
AdminOfferingsView — the Course Offerings section of the Admin dashboard.

Shows all scheduled course sections with enrollment/capacity/waitlist
counts. Allows the admin to create new offerings by selecting a course
from the BST catalog.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from registrar import CourseOffering
from views.theme import (
    FONT_FAMILY, FONT_SMALL,
    BG_SURFACE,
    ACCENT, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM,
    TREEVIEW_BG, TREEVIEW_ALT,
)


class AdminOfferingsView(ttk.Frame):
    """
    Ttk frame that renders the Course Offerings admin panel.

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

    # ── Build ─────────────────────────────────────────────────────────

    def _build(self):
        # Section header
        hdr = ttk.Frame(self, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=16)
        ttk.Label(hdr_inner, text="Course Offerings",
                  font=(FONT_FAMILY, 16, "bold"), foreground=TEXT_PRIMARY,
                  style="Surface.TLabel").pack(side="left")
        ttk.Label(hdr_inner, text="Scheduled sections & enrollment",
                  font=FONT_SMALL, foreground=TEXT_DIM,
                  style="Surface.TLabel").pack(side="left", padx=12)
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        # Create-offering form
        card = ttk.Frame(self, style="Surface.TFrame")
        card.pack(fill="x", padx=20, pady=16)
        ttk.Label(card, text="Schedule New Offering",
                  font=(FONT_FAMILY, 10, "bold"), foreground=ACCENT,
                  style="Surface.TLabel").pack(anchor="w", pady=(0, 8))

        fields = ttk.Frame(card, style="Surface.TFrame")
        fields.pack(fill="x")
        labels = ["Course (BST)", "Section", "Year", "Quarter", "Capacity", "Time Slot"]
        for i, lbl in enumerate(labels):
            ttk.Label(fields, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel"
                      ).grid(row=0, column=i, padx=5, sticky="w")

        catalog_names = [c.name for c in self.uni.catalog.inorder()]
        self._course   = ttk.Combobox(fields, values=catalog_names,
                                      width=20, state="readonly")
        self._section  = ttk.Entry(fields, width=5)
        self._section.insert(0, "1")
        self._year     = ttk.Entry(fields, width=6)
        self._year.insert(0, "2026")
        self._quarter  = ttk.Combobox(fields,
                                      values=["Fall", "Winter", "Spring", "Summer"],
                                      width=8, state="readonly")
        self._quarter.set("Spring")
        self._capacity = ttk.Entry(fields, width=5)
        self._capacity.insert(0, "30")
        self._time     = ttk.Combobox(fields, values=[
            "MW 08:00-09:30", "MW 10:00-11:30", "MW 12:00-13:30", "MW 14:00-15:30",
            "TR 08:00-09:30", "TR 09:00-10:30", "TR 10:00-11:30", "TR 14:00-15:30",
        ], width=16)
        self._time.set("MW 10:00-11:30")

        for i, w in enumerate([self._course, self._section, self._year,
                                self._quarter, self._capacity, self._time]):
            w.grid(row=1, column=i, padx=5, pady=(4, 0), sticky="ew")
        ttk.Button(fields, text="📅 Create", style="Accent.TButton",
                   command=self._create_offering).grid(row=1, column=6, padx=(12, 0))

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20)

        # Offerings treeview
        tree_wrap = ttk.Frame(self, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("id", "course", "section", "quarter", "time",
                "enrolled", "capacity", "waitlist")
        self._tree = ttk.Treeview(tree_wrap, columns=cols,
                                  show="headings", selectmode="browse")
        for col, heading, w in [
            ("id",       "#",        40),  ("course",   "Course",   190),
            ("section",  "Sec",      50),  ("quarter",  "Quarter",  95),
            ("time",     "Time Slot",140), ("enrolled", "Enrolled", 75),
            ("capacity", "Cap",      55),  ("waitlist", "Waitlist", 65),
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=w, anchor="center")

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.refresh()

    # ── Actions ───────────────────────────────────────────────────────

    def _create_offering(self):
        course_name = self._course.get()
        if not course_name:
            messagebox.showwarning("Validation", "Select a course from the BST catalog.")
            return
        course = self.uni.catalog.search(course_name)
        if not course:
            messagebox.showerror("Error", "Course not found in BST.")
            return
        try:
            section  = int(self._section.get())
            year     = int(self._year.get())
            capacity = int(self._capacity.get())
        except ValueError:
            messagebox.showwarning("Validation",
                                   "Section, Year, and Capacity must be numbers.")
            return

        offering = CourseOffering(course, section, year,
                                  self._quarter.get(), capacity, self._time.get())
        self.uni.offerings.append(offering)
        self.uni._save()
        self.refresh()
        self.app._refresh_header_stats()
        self.app._set_status(
            f"Offering created: {offering.display_name} ({self._quarter.get()} {year})"
        )

    # ── Refresh ───────────────────────────────────────────────────────

    def refresh(self):
        """Rebuild the offerings treeview from the current data."""
        for item in self._tree.get_children():
            self._tree.delete(item)
        for i, o in enumerate(self.uni.offerings):
            tag = "even" if i % 2 == 0 else "odd"
            self._tree.insert("", "end", values=(
                i + 1, o.course.name, o.section,
                f"{o.quarter} {o.year}", o.time_slot,
                len(o.enrolled_students), o.capacity, len(o.waitlist),
            ), tags=(tag,))
        self._tree.tag_configure("even", background=TREEVIEW_BG)
        self._tree.tag_configure("odd",  background=TREEVIEW_ALT)
