"""StudentTranscriptView showing completed courses and grades."""

from tkinter import ttk

from registrar.models import GPA_SCALE
from views.theme import (
    FONT_FAMILY,
    TEXT_PRIMARY,
    TREEVIEW_BG, TREEVIEW_ALT,
)


class StudentTranscriptView(ttk.Frame):
    """
    Ttk frame that renders the student's academic transcript.

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
        ttk.Label(hdr_inner, text="Transcript",
                  font=(FONT_FAMILY, 15, "bold"), foreground=TEXT_PRIMARY,
                  style="Surface.TLabel").pack(side="left")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        tree_wrap = ttk.Frame(self, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("course", "grade", "points")
        self._tree = ttk.Treeview(tree_wrap, columns=cols, show="headings")
        for col, heading, w, anchor in [
            ("course",  "Course Name",    0,   "w"),
            ("grade",   "Grade",          80,  "center"),
            ("points",  "Quality Points", 130, "center"),
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=w, anchor=anchor, stretch=(col == "course"))

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    # ── Refresh ───────────────────────────────────────────────────────

    def refresh(self):
        """Rebuild the transcript from the current student's completed_courses."""
        for item in self._tree.get_children():
            self._tree.delete(item)
        student = self.uni.students.get(self.app.current_user.username)
        if not student:
            return
        for i, (course, grade) in enumerate(student.completed_courses.items()):
            pts = GPA_SCALE.get(grade, 0.0)
            tag = "even" if i % 2 == 0 else "odd"
            self._tree.insert("", "end",
                              values=(course, grade, f"{pts:.1f}"),
                              tags=(tag,))
        self._tree.tag_configure("even", background=TREEVIEW_BG)
        self._tree.tag_configure("odd",  background=TREEVIEW_ALT)
