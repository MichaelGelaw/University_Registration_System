"""StudentDashboard container with sidebar and tabbed content."""

import tkinter as tk
from tkinter import ttk
from datetime import datetime

from views.student_transcript import StudentTranscriptView
from views.student_register   import StudentRegisterView
from views.student_schedule   import StudentScheduleView
from views.theme import (
    FONT_FAMILY,
    BG_CARD, BG_SURFACE,
    ACCENT,
    SUCCESS, WARNING, DANGER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM,
    BORDER,
)
from utils.image_processing import process_avatar


class StudentDashboard(ttk.Frame):
    """
    Full-height frame that holds the student profile sidebar and the
    three tabbed content views.

    After construction, ``app.student_dashboard`` is set so that child
    views (e.g. StudentRegisterView) can call
    ``self.app.student_dashboard.refresh_portal()`` after an enrollment.

    Parameters
    ----------
    parent : tk widget — the content_frame provided by UniversityApp
    app    : UniversityApp
    """

    def __init__(self, parent, app):
        super().__init__(parent, style="TFrame")
        self.app = app
        self.uni = app.uni
        app.student_dashboard = self    # register for child-view access
        self._active_section  = "transcript"
        self._build()

    # BUILD

    def _build(self):
        # LEFT PROFILE SIDEBAR
        self._sidebar = tk.Frame(self, bg=BG_CARD, width=220)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        # RIGHT CONTENT AREA
        right = ttk.Frame(self, style="TFrame")
        right.pack(side="left", fill="both", expand=True)

        # Top nav bar
        nav_bar = ttk.Frame(right, style="Surface.TFrame")
        nav_bar.pack(fill="x")
        ttk.Separator(right, orient="horizontal").pack(fill="x")

        self._nav_btns = {}
        nav_items = [
            ("transcript", "📜  Transcript"),
            ("register",   "📝  Register"),
            ("schedule",   "📅  My Schedule"),
        ]
        for key, label in nav_items:
            btn = tk.Label(nav_bar, text=label, bg=BG_SURFACE, fg=TEXT_SECONDARY,
                           font=(FONT_FAMILY, 10), padx=20, pady=12, cursor="hand2")
            btn.pack(side="left")
            btn.bind("<Button-1>", lambda e, k=key: self._show_section(k))
            btn.bind("<Enter>",    lambda e, b=btn: (
                b.config(fg=ACCENT) if b["bg"] == BG_SURFACE else None))
            btn.bind("<Leave>",    lambda e, b=btn, k2=key: b.config(
                fg=TEXT_SECONDARY if self._active_section != k2 else ACCENT))
            self._nav_btns[key] = btn

        # Instantiate the three section views
        self.transcript_view = StudentTranscriptView(right, self.app)
        self.register_view   = StudentRegisterView(right,   self.app)
        self.schedule_view   = StudentScheduleView(right,   self.app)

        # Populate the sidebar and show the default section
        self._rebuild_sidebar()
        self._show_section("transcript")

    # NAVIGATION

    def _show_section(self, key):
        """Hide all panels, show the requested one, and refresh it."""
        self._active_section = key
        section_map = {
            "transcript": self.transcript_view,
            "register":   self.register_view,
            "schedule":   self.schedule_view,
        }
        for frame in section_map.values():
            frame.pack_forget()
        section_map[key].pack(fill="both", expand=True)

        # Lazy refresh — only the visible section is updated
        section_map[key].refresh()

        for k, btn in self._nav_btns.items():
            if k == key:
                btn.config(fg=ACCENT, font=(FONT_FAMILY, 10, "bold"), relief="flat", bd=0)
            else:
                btn.config(fg=TEXT_SECONDARY, font=(FONT_FAMILY, 10), relief="flat", bd=0)

    # SIDEBAR

    def _rebuild_sidebar(self):
        """Destroy and rebuild the profile sidebar with fresh data."""
        for widget in self._sidebar.winfo_children():
            widget.destroy()

        student = self.uni.students.get(self.app.current_user.username)
        if not student:
            return

        # Avatar
        avatar_frame = tk.Frame(self._sidebar, bg=BG_CARD)
        avatar_frame.pack(fill="x", pady=(28, 0))
        self._avatar_img = process_avatar(
            getattr(student, "avatar_path", ""), size=(88, 88))
        if self._avatar_img:
            av_lbl = tk.Label(avatar_frame, image=self._avatar_img, bg=BG_CARD)
        else:
            av_lbl = tk.Label(avatar_frame, text="👤",
                              font=(FONT_FAMILY, 42), bg=BG_CARD)
        av_lbl.pack()

        # Name & username
        tk.Label(self._sidebar, text=student.full_name, bg=BG_CARD,
                 fg=TEXT_PRIMARY, font=(FONT_FAMILY, 12, "bold"),
                 wraplength=190, justify="center").pack(pady=(10, 2))
        tk.Label(self._sidebar, text=f"@{student.username}", bg=BG_CARD,
                 fg=TEXT_DIM, font=(FONT_FAMILY, 9)).pack()

        # Age
        try:
            dob_dt = datetime.strptime(student.dob, "%Y-%m-%d")
            today  = datetime.today()
            age    = today.year - dob_dt.year - (
                (today.month, today.day) < (dob_dt.month, dob_dt.day))
            tk.Label(self._sidebar, text=f"Age {age}", bg=BG_CARD,
                     fg=TEXT_DIM, font=(FONT_FAMILY, 9)).pack(pady=(2, 0))
        except Exception:
            pass

        # Divider
        tk.Frame(self._sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=18)

        # Count waitlisted offerings
        waitlisted = sum(
            1 for o in self.uni.offerings
            if student.username in o.waitlist
        )

        gpa_color = (SUCCESS if student.gpa >= 3.5
                     else WARNING if student.gpa >= 2.5 else DANGER)
        for val, label, color in [
            (f"{student.gpa:.2f}",                "GPA",        gpa_color),
            (str(len(student.completed_courses)),  "Completed",  ACCENT),
            (str(len(student.active_schedule)),    "Active",     WARNING),
            (str(waitlisted),                      "Waitlisted", DANGER),
        ]:
            stat_frame = tk.Frame(self._sidebar, bg=BG_CARD)
            stat_frame.pack(fill="x", padx=24, pady=6)
            tk.Label(stat_frame, text=val, bg=BG_CARD, fg=color,
                     font=(FONT_FAMILY, 20, "bold")).pack(anchor="w")
            tk.Label(stat_frame, text=label, bg=BG_CARD, fg=TEXT_DIM,
                     font=(FONT_FAMILY, 8)).pack(anchor="w")

        # Divider
        tk.Frame(self._sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=18)

        # Email
        if student.email:
            tk.Label(self._sidebar, text="Email", bg=BG_CARD, fg=TEXT_DIM,
                     font=(FONT_FAMILY, 8, "bold")).pack(anchor="w", padx=24)
            tk.Label(self._sidebar, text=student.email, bg=BG_CARD,
                     fg=TEXT_SECONDARY, font=(FONT_FAMILY, 9),
                     wraplength=185, justify="left").pack(anchor="w", padx=24, pady=(2, 0))

    # PUBLIC API

    def refresh_portal(self):
        """
        Called after any data mutation (enrollment, drop, grade) to
        update the sidebar stats and refresh the currently visible section.
        """
        self._rebuild_sidebar()
        # Refresh only the active section; others refresh lazily on navigation
        refresh_map = {
            "transcript": self.transcript_view.refresh,
            "register":   self.register_view.refresh,
            "schedule":   self.schedule_view.refresh,
        }
        refresh_map[self._active_section]()
