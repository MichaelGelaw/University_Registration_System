"""AdminCatalogView for browsing and managing catalog courses."""

import tkinter as tk
from tkinter import ttk, messagebox

from registrar.models import Course
from views.theme import (
    FONT_FAMILY, FONT_SMALL, FONT_BODY, FONT_BUTTON,
    BG_DARK, BG_SURFACE, BG_CARD,
    ACCENT, DANGER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM,
    TREEVIEW_BG, TREEVIEW_ALT,
)


class AdminCatalogView(ttk.Frame):
    """Ttk frame that renders the Course Catalog admin panel."""

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
        ttk.Label(hdr_inner, text="Course Catalog", font=(FONT_FAMILY, 16, "bold"),
                  foreground=TEXT_PRIMARY, style="Surface.TLabel").pack(side="left")
        ttk.Label(hdr_inner, text="BST — sorted in-order", font=FONT_SMALL,
                  foreground=TEXT_DIM, style="Surface.TLabel").pack(side="left", padx=12)
        ttk.Button(hdr_inner, text="🗑  Delete Selected", style="Danger.TButton",
                   command=self._delete_course).pack(side="right")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        # Add-course form
        card = ttk.Frame(self, style="Surface.TFrame")
        card.pack(fill="x", padx=20, pady=16)
        ttk.Label(card, text="Add Course", font=(FONT_FAMILY, 10, "bold"),
                  foreground=ACCENT, style="Surface.TLabel").pack(anchor="w", pady=(0, 8))

        fields = ttk.Frame(card, style="Surface.TFrame")
        fields.pack(fill="x")
        field_defs = [
            ("Dept", 6), ("#", 5), ("Course Name", 22),
            ("Credits", 5), ("Prerequisites (comma-sep)", 26),
        ]
        for i, (lbl, _) in enumerate(field_defs):
            ttk.Label(fields, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel"
                      ).grid(row=0, column=i, padx=5, sticky="w")

        self._dept   = ttk.Entry(fields, width=field_defs[0][1])
        self._num    = ttk.Entry(fields, width=field_defs[1][1])
        self._name   = ttk.Entry(fields, width=field_defs[2][1])
        self._cred   = ttk.Entry(fields, width=field_defs[3][1])
        self._prereqs= ttk.Entry(fields, width=field_defs[4][1])
        for i, e in enumerate([self._dept, self._num, self._name,
                                self._cred, self._prereqs]):
            e.grid(row=1, column=i, padx=5, pady=(4, 0), sticky="ew")
        ttk.Button(fields, text="➕ Add Course", style="Accent.TButton",
                   command=self._add_course).grid(row=1, column=5, padx=(12, 0))

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20)

        # Catalog treeview
        tree_wrap = ttk.Frame(self, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("dept", "number", "name", "credits", "prereqs")
        self._tree = ttk.Treeview(tree_wrap, columns=cols,
                                  show="headings", selectmode="browse")
        for col, heading, w, anchor in [
            ("dept",    "Dept",          70,  "center"),
            ("number",  "#",             60,  "center"),
            ("name",    "Course Name",   230, "w"),
            ("credits", "Cr",            50,  "center"),
            ("prereqs", "Prerequisites", 0,   "w"),
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=w, anchor=anchor,
                              stretch=(col == "prereqs"))

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.refresh()

    # ACTIONS

    def _add_course(self):
        dept  = self._dept.get().strip().upper()
        num   = self._num.get().strip()
        name  = self._name.get().strip()
        cred  = self._cred.get().strip()
        prereqs_str = self._prereqs.get().strip()

        if not all([dept, num, name, cred]):
            messagebox.showwarning("Validation",
                                   "Department, Number, Name, and Credits are required.")
            return
        try:
            num  = int(num)
            cred = int(cred)
        except ValueError:
            messagebox.showwarning("Validation", "Number and Credits must be integers.")
            return

        prereqs = [p.strip() for p in prereqs_str.split(",") if p.strip()]
        self.uni.catalog.insert(Course(dept, num, name, cred, prereqs))
        self.uni._save()
        self.refresh()
        self.app._refresh_header_stats()
        self.app._set_status(f"Course '{name}' inserted into BST (O(log n)).")

        for e in [self._dept, self._num, self._name, self._cred, self._prereqs]:
            e.delete(0, "end")

    def _delete_course(self):
        sel = self._tree.focus()
        if not sel:
            return
        name = self._tree.item(sel)["values"][2]
        if messagebox.askyesno("Confirm", f"Delete '{name}' from BST?"):
            self.uni.catalog.delete(name)
            self.uni._save()
            self.refresh()
            self.app._refresh_header_stats()
            self.app._set_status(f"Course '{name}' removed from BST.")

    # REFRESH

    def refresh(self):
        """Rebuild the treeview from the current BST in-order traversal."""
        for item in self._tree.get_children():
            self._tree.delete(item)
        for i, c in enumerate(self.uni.catalog.inorder()):
            tag = "even" if i % 2 == 0 else "odd"
            prereqs_str = ", ".join(c.prereqs) if c.prereqs else "—"
            self._tree.insert("", "end",
                              values=(c.dept, c.number, c.name, c.credits, prereqs_str),
                              tags=(tag,))
        self._tree.tag_configure("even", background=TREEVIEW_BG)
        self._tree.tag_configure("odd",  background=TREEVIEW_ALT)
