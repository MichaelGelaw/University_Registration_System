"""AdminDashboard view with sidebar navigation and admin sections."""

import tkinter as tk
from tkinter import ttk

from views.admin_catalog   import AdminCatalogView
from views.admin_offerings import AdminOfferingsView
from views.admin_students  import AdminStudentsView
from views.admin_grades    import AdminGradesView
from views.theme import (
    FONT_FAMILY,
    ACCENT, ACCENT_HOVER, ACCENT_DIM,
)


class AdminDashboard(ttk.Frame):
    """
    Full-width frame that contains the admin sidebar + content area.

    After construction, ``app.admin_dashboard`` is set so that child
    views (e.g. AdminGradesView) can reach sibling views via
    ``self.app.admin_dashboard.students_view.refresh()``.

    Parameters
    ----------
    parent : tk widget — the content_frame provided by UniversityApp
    app    : UniversityApp — gives access to app.uni, app._set_status(), etc.
    """

    def __init__(self, parent, app):
        super().__init__(parent, style="TFrame")
        self.app = app
        app.admin_dashboard = self      # register so child views can reach siblings
        self._build()

    # ── Build ─────────────────────────────────────────────────────────

    def _build(self):
        # ── Left sidebar ──────────────────────────────────────────────
        sidebar = tk.Frame(self, bg=ACCENT, width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="⚙  Admin", bg=ACCENT, fg="#ffffff",
                 font=(FONT_FAMILY, 13, "bold"), pady=20).pack(fill="x")
        tk.Frame(sidebar, bg="#6366f1", height=1).pack(fill="x", padx=16)

        self._nav_btns  = {}
        self._active_key = "catalog"
        nav_items = [
            ("catalog",   "📚  Course Catalog"),
            ("offerings", "📅  Offerings"),
            ("students",  "👥  Students"),
            ("grades",    "📝  Grades & Drop"),
        ]
        for key, label in nav_items:
            btn = tk.Label(sidebar, text=label, bg=ACCENT, fg="#c7d2fe",
                           font=(FONT_FAMILY, 10), anchor="w",
                           padx=22, pady=13, cursor="hand2")
            btn.pack(fill="x")
            btn.bind("<Button-1>", lambda e, k=key: self._show_section(k))
            btn.bind("<Enter>",    lambda e, b=btn: b.config(bg=ACCENT_HOVER, fg="#ffffff"))
            btn.bind("<Leave>",    lambda e, b=btn, k2=key: b.config(
                bg="#3730a3" if self._active_key == k2 else ACCENT,
                fg="#ffffff"  if self._active_key == k2 else "#c7d2fe"))
            self._nav_btns[key] = btn

        # ── Right content area ────────────────────────────────────────
        content = ttk.Frame(self, style="TFrame")
        content.pack(side="left", fill="both", expand=True)

        # Instantiate all four section views (hidden initially)
        self.catalog_view   = AdminCatalogView(content,   self.app)
        self.offerings_view = AdminOfferingsView(content, self.app)
        self.students_view  = AdminStudentsView(content,  self.app)
        self.grades_view    = AdminGradesView(content,    self.app)

        # Show the default section
        self._show_section("catalog")

    # ── Navigation ────────────────────────────────────────────────────

    def _show_section(self, key):
        """Hide all section frames and reveal the requested one."""
        self._active_key = key
        section_map = {
            "catalog":   self.catalog_view,
            "offerings": self.offerings_view,
            "students":  self.students_view,
            "grades":    self.grades_view,
        }
        for frame in section_map.values():
            frame.pack_forget()
        section_map[key].pack(fill="both", expand=True)

        # Lazily refresh the section being navigated to
        section_map[key].refresh()

        # Update sidebar highlight
        for k, btn in self._nav_btns.items():
            btn.config(
                bg="#3730a3" if k == key else ACCENT,
                fg="#ffffff"  if k == key else "#c7d2fe",
            )
