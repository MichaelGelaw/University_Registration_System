import tkinter as tk
from tkinter import ttk, messagebox

from views.theme import (
    FONT_FAMILY, FONT_SMALL,
    BG_DARK, BG_SURFACE, BG_CARD,
    ACCENT, ACCENT_DIM, SUCCESS, DANGER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM,
    TREEVIEW_BG, TREEVIEW_ALT,
)

from registrar.models import GPA_SCALE
GRADES = list(GPA_SCALE.keys())


class AdminGradesView(ttk.Frame):
    """Grades & Drop panel with two independent sub-tabs."""

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
        ttk.Label(hdr_inner, text="Grades & Drop",
                  font=(FONT_FAMILY, 16, "bold"), foreground=TEXT_PRIMARY,
                  style="Surface.TLabel").pack(side="left")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        # Sub-tab bar
        tab_bar = ttk.Frame(self, style="Surface.TFrame")
        tab_bar.pack(fill="x")
        self._tab_frames = {}
        self._tab_btns   = {}

        container = ttk.Frame(self, style="TFrame")
        container.pack(fill="both", expand=True)

        for key, label in [("grades", "  📝  Grades  "), ("drop", "  🚫  Drop  ")]:
            frame = ttk.Frame(container, style="TFrame")
            self._tab_frames[key] = frame

            btn = tk.Label(tab_bar, text=label,
                           bg=BG_SURFACE, fg=TEXT_SECONDARY,
                           font=(FONT_FAMILY, 10), padx=8, pady=10,
                           cursor="hand2", relief="flat")
            btn.pack(side="left")
            btn.bind("<Button-1>", lambda e, k=key: self._switch_tab(k))
            self._tab_btns[key] = btn

        ttk.Separator(tab_bar, orient="horizontal").pack(side="bottom", fill="x")

        # Build each tab's content
        self._build_grades_tab(self._tab_frames["grades"])
        self._build_drop_tab(self._tab_frames["drop"])

        # Show grades tab by default
        self._switch_tab("grades")

    def _switch_tab(self, key):
        for k, frame in self._tab_frames.items():
            frame.pack_forget()
        self._tab_frames[key].pack(fill="both", expand=True)

        for k, btn in self._tab_btns.items():
            if k == key:
                btn.config(bg=BG_DARK, fg=ACCENT,
                           font=(FONT_FAMILY, 10, "bold"),
                           relief="flat")
            else:
                btn.config(bg=BG_SURFACE, fg=TEXT_SECONDARY,
                           font=(FONT_FAMILY, 10),
                           relief="flat")

    # GRADES TAB

    def _build_grades_tab(self, parent):
        # Toolbar: offering selector + Save button
        toolbar = ttk.Frame(parent, style="Surface.TFrame")
        toolbar.pack(fill="x", padx=20, pady=14)

        ttk.Label(toolbar, text="Class", font=(FONT_FAMILY, 9, "bold"),
                  foreground=TEXT_SECONDARY,
                  style="Surface.TLabel").pack(side="left", padx=(0, 6))

        self._grade_offering = ttk.Combobox(toolbar, width=36, state="readonly")
        self._grade_offering.pack(side="left", padx=(0, 12))
        self._grade_offering.bind("<<ComboboxSelected>>", self._on_grade_offering_change)

        ttk.Button(toolbar, text="Save Grades", style="Success.TButton",
                   command=self._save_all_grades).pack(side="left")

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=20)

        # Enrollment table for grades
        tree_wrap = ttk.Frame(parent, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=12)

        cols = ("student", "status", "current_grade", "new_grade")
        self._grade_tree = ttk.Treeview(tree_wrap, columns=cols,
                                        show="headings", selectmode="none")
        for col, heading, w, anchor in [
            ("student",       "Student",       0,   "w"),
            ("status",        "Status",        110, "center"),
            ("current_grade", "Current Grade", 110, "center"),
            ("new_grade",     "Assign Grade",  130, "center"),
        ]:
            self._grade_tree.heading(col, text=heading)
            self._grade_tree.column(col, width=w, anchor=anchor,
                                    stretch=(col == "student"))

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical",
                            command=self._grade_tree.yview)
        self._grade_tree.configure(yscrollcommand=vsb.set)
        self._grade_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Dict: iid -> StringVar for the grade combobox overlay
        self._grade_vars = {}
        self._grade_combos = {}

        # Track the overlay frame (comboboxes float outside the treeview)
        self._grade_tree.bind("<Configure>", self._reposition_grade_combos)

    def _on_grade_offering_change(self, event=None):
        self._refresh_grade_table()

    def _refresh_grade_table(self):
        # Destroy existing overlay comboboxes
        for cb in self._grade_combos.values():
            cb.destroy()
        self._grade_combos.clear()
        self._grade_vars.clear()

        for item in self._grade_tree.get_children():
            self._grade_tree.delete(item)

        idx = self._grade_offering.current()
        if idx < 0 or idx >= len(self.uni.offerings):
            return
        offering = self.uni.offerings[idx]

        for i, username in enumerate(offering.enrolled_students):
            current = offering.grades.get(username, "—")
            tag = "even" if i % 2 == 0 else "odd"
            iid = self._grade_tree.insert("", "end",
                values=(username, "Enrolled", current, ""),
                tags=(tag,))
            var = tk.StringVar(value=current if current != "—" else "")
            self._grade_vars[iid] = var

        self._grade_tree.tag_configure("even",     background=TREEVIEW_BG)
        self._grade_tree.tag_configure("odd",      background=TREEVIEW_ALT)

        self._grade_tree.update_idletasks()
        self._place_grade_combos()

    def _place_grade_combos(self):
        """Overlay a Combobox on the 'new_grade' cell for each enrolled row."""
        for cb in self._grade_combos.values():
            cb.destroy()
        self._grade_combos.clear()

        tree = self._grade_tree
        col_id = "#4"  # new_grade is the 4th column

        for iid, var in self._grade_vars.items():
            try:
                bbox = tree.bbox(iid, col_id)
            except Exception:
                continue
            if not bbox:
                continue
            x, y, w, h = bbox
            cb = ttk.Combobox(tree, values=GRADES, textvariable=var,
                              width=9, state="readonly",
                              font=(FONT_FAMILY, 9))
            cb.place(x=x, y=y, width=w, height=h)
            self._grade_combos[iid] = cb

    def _reposition_grade_combos(self, event=None):
        self._place_grade_combos()

    def _save_all_grades(self):
        idx = self._grade_offering.current()
        if idx < 0 or idx >= len(self.uni.offerings):
            messagebox.showwarning("Validation", "Please select a class first.")
            return
        offering = self.uni.offerings[idx]

        saved = 0
        for iid, var in self._grade_vars.items():
            grade = var.get().strip()
            if not grade:
                continue
            username = self._grade_tree.item(iid)["values"][0]
            self.uni.finalize_grade(username, offering, grade)
            saved += 1

        if saved == 0:
            messagebox.showwarning("No Grades", "No grades were entered.")
            return

        self._refresh_grade_table()
        self.app.admin_dashboard.students_view.refresh()
        # If a student is currently logged in, refresh their portal too
        if (self.app.current_role == "Student"
                and self.app.student_dashboard is not None):
            self.app.student_dashboard.refresh_portal()
        msg = f"Grades saved for {saved} student(s)."
        messagebox.showinfo("Grades Saved", msg)
        self.app._set_status(msg)

    # DROP TAB

    def _build_drop_tab(self, parent):
        # Toolbar: offering selector
        toolbar = ttk.Frame(parent, style="Surface.TFrame")
        toolbar.pack(fill="x", padx=20, pady=14)

        ttk.Label(toolbar, text="Class", font=(FONT_FAMILY, 9, "bold"),
                  foreground=TEXT_SECONDARY,
                  style="Surface.TLabel").pack(side="left", padx=(0, 6))

        self._drop_offering = ttk.Combobox(toolbar, width=36, state="readonly")
        self._drop_offering.pack(side="left")
        self._drop_offering.bind("<<ComboboxSelected>>", self._on_drop_offering_change)

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=20)

        # Enrollment table for drop
        tree_wrap = ttk.Frame(parent, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=12)

        cols = ("student", "status", "grade", "action")
        self._drop_tree = ttk.Treeview(tree_wrap, columns=cols,
                                       show="headings", selectmode="none")
        for col, heading, w, anchor in [
            ("student", "Student", 0,   "w"),
            ("status",  "Status",  110, "center"),
            ("grade",   "Grade",   90,  "center"),
            ("action",  "",        110, "center"),
        ]:
            self._drop_tree.heading(col, text=heading)
            self._drop_tree.column(col, width=w, anchor=anchor,
                                   stretch=(col == "student"))

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical",
                            command=self._drop_tree.yview)
        self._drop_tree.configure(yscrollcommand=vsb.set)
        self._drop_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Overlay drop buttons
        self._drop_btns = {}
        self._drop_tree.bind("<Configure>", self._reposition_drop_btns)

    def _on_drop_offering_change(self, event=None):
        self._refresh_drop_table()

    def _refresh_drop_table(self):
        for btn in self._drop_btns.values():
            btn.destroy()
        self._drop_btns.clear()

        for item in self._drop_tree.get_children():
            self._drop_tree.delete(item)

        idx = self._drop_offering.current()
        if idx < 0 or idx >= len(self.uni.offerings):
            return
        offering = self.uni.offerings[idx]

        for i, username in enumerate(offering.enrolled_students):
            grade = offering.grades.get(username, "—")
            tag = "even" if i % 2 == 0 else "odd"
            iid = self._drop_tree.insert("", "end",
                values=(username, "Enrolled", grade, ""),
                tags=(tag,))
            self._make_drop_btn(iid, username, offering)

        for i, username in enumerate(offering.waitlist.to_list()):
            tag = "waitlist"
            iid = self._drop_tree.insert("", "end",
                values=(username, f"Waitlist #{i+1}", "—", ""),
                tags=(tag,))
            self._make_drop_btn(iid, username, offering)

        self._drop_tree.tag_configure("even",     background=TREEVIEW_BG)
        self._drop_tree.tag_configure("odd",      background=TREEVIEW_ALT)
        self._drop_tree.tag_configure("waitlist", background="#fef3c7",
                                      foreground="#92400e")

        self._drop_tree.update_idletasks()
        self._place_drop_btns()

    def _make_drop_btn(self, iid, username, offering):
        btn = tk.Button(
            self._drop_tree,
            text="Drop",
            bg=DANGER, fg="#ffffff",
            font=(FONT_FAMILY, 8, "bold"),
            relief="flat", bd=0,
            cursor="hand2",
            activebackground="#b91c1c",
            activeforeground="#ffffff",
            command=lambda u=username, o=offering: self._confirm_drop(u, o)
        )
        self._drop_btns[iid] = btn

    def _place_drop_btns(self):
        tree = self._drop_tree
        col_id = "#4"
        for iid, btn in self._drop_btns.items():
            try:
                bbox = tree.bbox(iid, col_id)
            except Exception:
                continue
            if not bbox:
                continue
            x, y, w, h = bbox
            pad = 6
            btn.place(x=x + pad, y=y + 2,
                      width=w - pad * 2, height=h - 4)

    def _reposition_drop_btns(self, event=None):
        self._place_drop_btns()

    def _confirm_drop(self, username, offering):
        if not messagebox.askyesno(
            "Confirm Drop",
            f"Drop '{username}' from {offering.display_name}?\n\n"
            "If there is a student on the waitlist, they will be enrolled automatically."
        ):
            return
        result = self.uni.drop_student(username, offering)
        self.uni._save()
        self._refresh_drop_table()
        self._refresh_grade_table()  # keep grade tab in sync
        self.app.admin_dashboard.students_view.refresh()
        self.app.admin_dashboard.offerings_view.refresh()
        msg = result
        messagebox.showinfo("Drop Student", msg)
        self.app._set_status(msg)

    # REFRESH

    def refresh(self):
        """Called when the panel is navigated to."""
        offering_names = [
            f"{o.display_name} ({o.quarter} {o.year})" for o in self.uni.offerings
        ]
        self._grade_offering.config(values=offering_names)
        self._drop_offering.config(values=offering_names)
