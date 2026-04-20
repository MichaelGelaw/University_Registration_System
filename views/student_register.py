"""StudentRegisterView for enrolling in course offerings."""

from tkinter import ttk, messagebox

from views.theme import (
    FONT_FAMILY, FONT_SMALL,
    TEXT_PRIMARY, TEXT_SECONDARY,
    TREEVIEW_BG, TREEVIEW_ALT,
)


class StudentRegisterView(ttk.Frame):
    """
    Ttk frame that renders the course registration panel.

    Parameters
    ----------
    parent : tk widget — container provided by StudentDashboard
    app    : UniversityApp — access to app.uni, app.current_user,
             and app.student_dashboard for post-enrollment refresh
    """

    def __init__(self, parent, app):
        super().__init__(parent, style="TFrame")
        self.app = app
        self.uni = app.uni
        self._build()

    # ── Build ─────────────────────────────────────────────────────────

    def _build(self):
        hdr = ttk.Frame(self, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=14)
        ttk.Label(hdr_inner, text="Course Registration",
                  font=(FONT_FAMILY, 15, "bold"), foreground=TEXT_PRIMARY,
                  style="Surface.TLabel").pack(side="left")
        ttk.Button(hdr_inner, text="📝  Enroll in Selected",
                   style="Accent.TButton",
                   command=self._request_enrollment).pack(side="right")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        tree_wrap = ttk.Frame(self, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("id", "course", "time", "seats", "waitlist", "status")
        self._tree = ttk.Treeview(tree_wrap, columns=cols,
                                  show="headings", selectmode="browse")
        for col, heading, w, anchor in [
            ("id",       "#",        40,  "center"),
            ("course",   "Course",   0,   "w"),
            ("time",     "Time Slot",140, "center"),
            ("seats",    "Seats",    70,  "center"),
            ("waitlist", "Waitlist", 70,  "center"),
            ("status",   "Status",   130, "center"),
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=w, anchor=anchor, stretch=(col == "course"))

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._status_label = ttk.Label(self, text="", font=FONT_SMALL,
                                       foreground=TEXT_SECONDARY)
        self._status_label.pack(anchor="w", padx=20, pady=(0, 8))

    # ── Actions ───────────────────────────────────────────────────────

    def _request_enrollment(self):
        sel = self._tree.focus()
        if not sel:
            messagebox.showwarning("Selection", "Please select a course offering.")
            return
        vals = self._tree.item(sel)["values"]
        idx  = int(vals[0]) - 1
        if idx < 0 or idx >= len(self.uni.offerings):
            return

        offering = self.uni.offerings[idx]
        username = self.app.current_user.username
        result   = self.uni.register_student(username, offering)

        if "SUCCESS" in result:
            messagebox.showinfo("Enrollment", result)
        elif "WAITLIST" in result:
            messagebox.showinfo("Waitlist (FCFS Queue)", result)
        else:
            messagebox.showwarning("Registration Failed", result)

        # Refresh the student portal (sidebar stats + the active section)
        self.app.student_dashboard.refresh_portal()
        self._status_label.config(text=result)
        self.app._set_status(result)

    # ── Refresh ───────────────────────────────────────────────────────

    def refresh(self):
        """Rebuild the offerings list with up-to-date enrollment status."""
        for item in self._tree.get_children():
            self._tree.delete(item)
        username = self.app.current_user.username
        student  = self.uni.students.get(username)
        if not student:
            return

        for i, o in enumerate(self.uni.offerings):
            seats = o.seats_available
            wl    = len(o.waitlist)
            if username in o.enrolled_students:
                status = "✅ Enrolled"
            elif username in o.waitlist:
                pos    = o.waitlist.position_of(username)
                status = f"⏳ Waitlist #{pos}"
            else:
                status = "Available" if not o.is_full else "Full"

            if "Enrolled" in status:
                tag = "enrolled"
            elif "Waitlist" in status:
                tag = "waitlist_row"
            else:
                tag = "even" if i % 2 == 0 else "odd"

            self._tree.insert("", "end", values=(
                i + 1,
                f"{o.course.dept} {o.course.number}: {o.course.name}",
                o.time_slot,
                max(seats, 0),
                wl,
                status,
            ), tags=(tag,))

        self._tree.tag_configure("even",         background=TREEVIEW_BG)
        self._tree.tag_configure("odd",          background=TREEVIEW_ALT)
        self._tree.tag_configure("enrolled",     background="#dcfce7", foreground="#166534")
        self._tree.tag_configure("waitlist_row", background="#fef3c7", foreground="#92400e")
