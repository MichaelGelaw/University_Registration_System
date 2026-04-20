"""StudentScheduleView displaying the student's active schedule."""

from tkinter import ttk

from views.theme import (
    FONT_FAMILY,
    TEXT_PRIMARY,
    TREEVIEW_BG, TREEVIEW_ALT,
)


class StudentScheduleView(ttk.Frame):
    """
    Ttk frame that renders the student's active course schedule.

    Parameters
    ----------
    parent : tk widget — container provided by StudentDashboard
    app    : UniversityApp — access to app.uni and app.current_user
    """

    def __init__(self, parent, app):
        super().__init__(parent, style="TFrame")
        self.app = app
        self.uni = app.uni
        self._build()

    # BUILD

    def _build(self):
        hdr = ttk.Frame(self, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=14)
        ttk.Label(hdr_inner, text="My Schedule",
                  font=(FONT_FAMILY, 15, "bold"), foreground=TEXT_PRIMARY,
                  style="Surface.TLabel").pack(side="left")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        cols = ("course", "section", "time", "quarter")
        self._tree = ttk.Treeview(self, columns=cols, show="headings")
        for col, heading, w in [
            ("course",  "Course",   250),
            ("section", "Section",   70),
            ("time",    "Time Slot", 150),
            ("quarter", "Quarter",   120),
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=w, anchor="center")
        self._tree.pack(fill="both", expand=True, padx=15, pady=15)

    # REFRESH

    def refresh(self):
        """
        Rebuild the schedule table.

        Builds a display_name → offering dict in O(n) so each of the
        student's schedule entries is resolved in O(1) rather than
        scanning the full offerings list every time.
        """
        for item in self._tree.get_children():
            self._tree.delete(item)
        student = self.uni.students.get(self.app.current_user.username)
        if not student:
            return

        # O(n) lookup table — avoids O(n²) nested loop
        offering_lookup = {o.display_name: o for o in self.uni.offerings}

        for i, offering_name in enumerate(student.active_schedule):
            o = offering_lookup.get(offering_name)
            if o:
                tag = "even" if i % 2 == 0 else "odd"
                self._tree.insert("", "end", values=(
                    o.course.name, o.section, o.time_slot, f"{o.quarter} {o.year}"
                ), tags=(tag,))

        self._tree.tag_configure("even", background=TREEVIEW_BG)
        self._tree.tag_configure("odd",  background=TREEVIEW_ALT)
