"""
University Registration System — Modern Tkinter Desktop App
Uses custom DSA structures: BST (catalog), LinkedQueue (waitlists), MergeSort, Linear Search.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from registrar import Institution, Course, CourseOffering, Student

# ─── Color Palette (Modern Light Theme) ─────────────────────
BG_DARK       = "#f0f2f5"       # Main background — soft gray
BG_SURFACE    = "#ffffff"       # Surface panels — white
BG_CARD       = "#f8f9fc"       # Card backgrounds — very light blue-gray
BG_INPUT      = "#ffffff"       # Input fields — white
ACCENT        = "#4f46e5"       # Primary accent — indigo
ACCENT_HOVER  = "#6366f1"       # Hover state
ACCENT_DIM    = "#818cf8"       # Softer accent for tabs
SUCCESS       = "#16a34a"       # Green
WARNING       = "#d97706"       # Amber
DANGER        = "#dc2626"       # Red
TEXT_PRIMARY   = "#1e293b"      # Near-black text
TEXT_SECONDARY = "#475569"      # Slate-gray
TEXT_DIM       = "#94a3b8"      # Light slate
BORDER         = "#e2e8f0"      # Soft border
TREEVIEW_BG    = "#ffffff"      # White rows
TREEVIEW_FG    = "#1e293b"      # Dark text
TREEVIEW_SEL   = "#4f46e5"      # Indigo selection
TREEVIEW_ALT   = "#f1f5f9"      # Alternating row — light slate

FONT_FAMILY   = "Segoe UI"
FONT_HEADING  = (FONT_FAMILY, 20, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 13)
FONT_BODY     = (FONT_FAMILY, 10)
FONT_SMALL    = (FONT_FAMILY, 9)
FONT_BUTTON   = (FONT_FAMILY, 10, "bold")
FONT_TAB      = (FONT_FAMILY, 11, "bold")


def configure_styles():
    """Apply a modern light theme to all ttk widgets."""
    style = ttk.Style()
    style.theme_use("clam")

    # ── Global defaults ──
    style.configure(".", background=BG_DARK, foreground=TEXT_PRIMARY, font=FONT_BODY,
                    borderwidth=0, focuscolor=ACCENT)

    # ── Notebook (main tabs) ──
    style.configure("TNotebook", background=BG_DARK, borderwidth=0, padding=0)
    style.configure("TNotebook.Tab", background=BG_SURFACE, foreground=TEXT_SECONDARY,
                    padding=[24, 10], font=FONT_TAB)
    style.map("TNotebook.Tab",
              background=[("selected", ACCENT), ("active", ACCENT_DIM)],
              foreground=[("selected", "#ffffff"), ("active", TEXT_PRIMARY)],
              relief=[("selected", "flat")])

    # ── Inner tabs ──
    style.configure("Inner.TNotebook", background=BG_SURFACE, borderwidth=0)
    style.configure("Inner.TNotebook.Tab", background=BG_CARD, foreground=TEXT_SECONDARY,
                    padding=[18, 8], font=FONT_BODY)
    style.map("Inner.TNotebook.Tab",
              background=[("selected", ACCENT_DIM), ("active", BG_CARD)],
              foreground=[("selected", "#ffffff"), ("active", TEXT_PRIMARY)],
              relief=[("selected", "flat")])

    # ── Labels ──
    style.configure("TLabel", background=BG_DARK, foreground=TEXT_PRIMARY)
    style.configure("Card.TLabel", background=BG_CARD)
    style.configure("Surface.TLabel", background=BG_SURFACE)
    style.configure("Heading.TLabel", font=FONT_HEADING, foreground=TEXT_PRIMARY, background=BG_DARK)
    style.configure("Subtitle.TLabel", font=FONT_SUBTITLE, foreground=TEXT_SECONDARY, background=BG_DARK)
    style.configure("Accent.TLabel", foreground=ACCENT, background=BG_CARD, font=(FONT_FAMILY, 22, "bold"))
    style.configure("Value.TLabel", foreground=TEXT_PRIMARY, background=BG_CARD, font=(FONT_FAMILY, 11))
    style.configure("Dim.TLabel", foreground=TEXT_DIM, background=BG_CARD, font=FONT_SMALL)

    # ── Frames ──
    style.configure("TFrame", background=BG_DARK)
    style.configure("Card.TFrame", background=BG_CARD)
    style.configure("Surface.TFrame", background=BG_SURFACE)

    # ── Label Frames ──
    style.configure("TLabelframe", background=BG_SURFACE, foreground=ACCENT,
                    font=(FONT_FAMILY, 11, "bold"), borderwidth=1, relief="groove")
    style.configure("TLabelframe.Label", background=BG_SURFACE, foreground=ACCENT)

    # ── Buttons ──
    style.configure("Accent.TButton", background=ACCENT, foreground="#ffffff",
                    font=FONT_BUTTON, padding=[16, 8], borderwidth=0)
    style.map("Accent.TButton",
              background=[("active", ACCENT_HOVER), ("pressed", ACCENT_DIM)])

    style.configure("Danger.TButton", background=DANGER, foreground="#ffffff",
                    font=FONT_BUTTON, padding=[16, 8])
    style.map("Danger.TButton",
              background=[("active", "#ff6b6b"), ("pressed", "#c0392b")])

    style.configure("Success.TButton", background=SUCCESS, foreground="#ffffff",
                    font=FONT_BUTTON, padding=[16, 8])
    style.map("Success.TButton",
              background=[("active", "#58d68d"), ("pressed", "#27ae60")])

    style.configure("TButton", background="#e2e8f0", foreground=TEXT_PRIMARY,
                    font=FONT_BUTTON, padding=[14, 7])
    style.map("TButton", background=[("active", "#cbd5e1")])

    # ── Entry ──
    style.configure("TEntry", fieldbackground=BG_INPUT, foreground=TEXT_PRIMARY,
                    insertcolor=TEXT_PRIMARY, borderwidth=1, padding=[8, 6],
                    relief="solid", bordercolor=BORDER)
    style.map("TEntry", fieldbackground=[("focus", "#ffffff")],
              bordercolor=[("focus", ACCENT)])

    # ── Combobox ──
    style.configure("TCombobox", fieldbackground=BG_INPUT, foreground=TEXT_PRIMARY,
                    selectbackground=ACCENT, selectforeground="#ffffff",
                    padding=[8, 6], arrowcolor=ACCENT)
    style.map("TCombobox", fieldbackground=[("focus", BG_CARD)])

    # ── Treeview ──
    style.configure("Treeview", background=TREEVIEW_BG, foreground=TREEVIEW_FG,
                    fieldbackground=TREEVIEW_BG, borderwidth=0, rowheight=32,
                    font=FONT_BODY)
    style.configure("Treeview.Heading", background="#e8eaf0", foreground=ACCENT,
                    font=(FONT_FAMILY, 10, "bold"), borderwidth=1, padding=[8, 6],
                    relief="flat")
    style.map("Treeview",
              background=[("selected", TREEVIEW_SEL)],
              foreground=[("selected", "#ffffff")])
    style.map("Treeview.Heading",
              background=[("active", ACCENT_DIM)])

    # ── Scrollbar ──
    style.configure("Vertical.TScrollbar", background=BG_SURFACE,
                    troughcolor=BG_DARK, arrowcolor=ACCENT, borderwidth=0)

    # ── Separator ──
    style.configure("TSeparator", background=BORDER)

    return style


class UniversityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 University Registration System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=BG_DARK)

        # Set window icon background
        self.root.option_add("*TCombobox*Listbox.background", BG_INPUT)
        self.root.option_add("*TCombobox*Listbox.foreground", TEXT_PRIMARY)
        self.root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")

        self.style = configure_styles()

        # Load institution from JSON (rehydrates BST, Students, Queues)
        self.uni = Institution.load()

        self._build_header()
        self._build_notebook()
        self._build_status_bar()

    # ═══════════════════════════════════════════════════════════
    #  HEADER
    # ═══════════════════════════════════════════════════════════

    def _build_header(self):
        header = ttk.Frame(self.root, style="Surface.TFrame")
        header.pack(fill="x", padx=0, pady=0)

        inner = ttk.Frame(header, style="Surface.TFrame")
        inner.pack(fill="x", padx=30, pady=(16, 12))

        ttk.Label(inner, text="🎓", font=(FONT_FAMILY, 28), style="Surface.TLabel").pack(side="left", padx=(0, 10))

        text_block = ttk.Frame(inner, style="Surface.TFrame")
        text_block.pack(side="left")
        ttk.Label(text_block, text=self.uni.name, font=(FONT_FAMILY, 18, "bold"),
                  foreground=TEXT_PRIMARY, style="Surface.TLabel").pack(anchor="w")
        ttk.Label(text_block, text="Academic Management System  ·  Powered by Custom DSA",
                  font=FONT_SMALL, foreground=TEXT_DIM, style="Surface.TLabel").pack(anchor="w")

        # Stats on the right
        stats = ttk.Frame(inner, style="Surface.TFrame")
        stats.pack(side="right")
        n_courses = len(self.uni.catalog)
        n_students = len(self.uni.students)
        n_offerings = len(self.uni.offerings)
        for label, val, color in [("Courses", n_courses, ACCENT), ("Students", n_students, SUCCESS),
                                   ("Offerings", n_offerings, WARNING)]:
            chip = ttk.Frame(stats, style="Surface.TFrame")
            chip.pack(side="left", padx=12)
            ttk.Label(chip, text=str(val), font=(FONT_FAMILY, 16, "bold"),
                      foreground=color, style="Surface.TLabel").pack()
            ttk.Label(chip, text=label, font=FONT_SMALL,
                      foreground=TEXT_DIM, style="Surface.TLabel").pack()

    # ═══════════════════════════════════════════════════════════
    #  MAIN NOTEBOOK
    # ═══════════════════════════════════════════════════════════

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.tab_admin = ttk.Frame(self.notebook, style="TFrame")
        self.tab_student = ttk.Frame(self.notebook, style="TFrame")

        self.notebook.add(self.tab_admin, text="  ⚙  Admin Portal  ")
        self.notebook.add(self.tab_student, text="  🎒  Student Portal  ")
        self.notebook.pack(expand=True, fill="both", padx=15, pady=(5, 10))

        self._build_admin_tab()
        self._build_student_tab()

    def _build_status_bar(self):
        bar = ttk.Frame(self.root, style="Surface.TFrame")
        bar.pack(fill="x", side="bottom")
        self.status_label = ttk.Label(bar, text="  System ready  ·  All data structures loaded from JSON",
                                      font=FONT_SMALL, foreground=TEXT_DIM, style="Surface.TLabel")
        self.status_label.pack(side="left", padx=15, pady=4)
        ttk.Label(bar, text="BST · LinkedQueue · MergeSort · LinearSearch  ",
                  font=FONT_SMALL, foreground=ACCENT_DIM, style="Surface.TLabel").pack(side="right", padx=15, pady=4)

    def _set_status(self, msg):
        self.status_label.config(text=f"  {msg}")

    # ═══════════════════════════════════════════════════════════
    #  ADMIN TAB
    # ═══════════════════════════════════════════════════════════

    def _build_admin_tab(self):
        admin_nb = ttk.Notebook(self.tab_admin, style="Inner.TNotebook")
        admin_nb.pack(fill="both", expand=True, padx=10, pady=10)

        # Sub-tabs
        self.admin_catalog_tab = ttk.Frame(admin_nb, style="TFrame")
        self.admin_offerings_tab = ttk.Frame(admin_nb, style="TFrame")
        self.admin_students_tab = ttk.Frame(admin_nb, style="TFrame")
        self.admin_grades_tab = ttk.Frame(admin_nb, style="TFrame")

        admin_nb.add(self.admin_catalog_tab, text=" 📚 Course Catalog ")
        admin_nb.add(self.admin_offerings_tab, text=" 📅 Offerings ")
        admin_nb.add(self.admin_students_tab, text=" 👥 Students ")
        admin_nb.add(self.admin_grades_tab, text=" 📝 Grades & Drop ")

        self._build_admin_catalog()
        self._build_admin_offerings()
        self._build_admin_students()
        self._build_admin_grades()

    # ─── Catalog ─────────────────────────────────────────────

    def _build_admin_catalog(self):
        parent = self.admin_catalog_tab

        # Form
        form = ttk.LabelFrame(parent, text="  Add Course to BST Catalog  ")
        form.pack(fill="x", padx=15, pady=(15, 5))

        fields = ttk.Frame(form, style="TFrame")
        fields.pack(fill="x", padx=15, pady=12)

        for i, (lbl, w) in enumerate([("Department", 8), ("Number", 6), ("Course Name", 20),
                                       ("Credits", 5), ("Prerequisites (comma-sep)", 25)]):
            ttk.Label(fields, text=lbl, font=FONT_SMALL, foreground=TEXT_SECONDARY).grid(row=0, column=i, padx=6, sticky="w")

        self.cat_dept = ttk.Entry(fields, width=8)
        self.cat_num = ttk.Entry(fields, width=6)
        self.cat_name = ttk.Entry(fields, width=20)
        self.cat_cred = ttk.Entry(fields, width=5)
        self.cat_prereqs = ttk.Entry(fields, width=25)

        for i, e in enumerate([self.cat_dept, self.cat_num, self.cat_name, self.cat_cred, self.cat_prereqs]):
            e.grid(row=1, column=i, padx=6, pady=(2, 0), sticky="ew")

        ttk.Button(fields, text="➕ Insert into BST", style="Accent.TButton",
                   command=self._add_course).grid(row=1, column=5, padx=(12, 0))

        # Treeview
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        cols = ("dept", "number", "name", "credits", "prereqs")
        self.catalog_tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        for col, heading, w in [("dept", "Dept", 70), ("number", "#", 60), ("name", "Course Name", 220),
                                 ("credits", "Cr", 50), ("prereqs", "Prerequisites", 250)]:
            self.catalog_tree.heading(col, text=heading)
            self.catalog_tree.column(col, width=w, anchor="center" if w < 100 else "w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.catalog_tree.yview)
        self.catalog_tree.configure(yscrollcommand=vsb.set)
        self.catalog_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Bottom bar
        bot = ttk.Frame(parent)
        bot.pack(fill="x", padx=15, pady=(0, 10))
        ttk.Button(bot, text="🗑  Delete Selected", style="Danger.TButton",
                   command=self._delete_course).pack(side="right")

        self._refresh_catalog_tree()

    def _add_course(self):
        dept = self.cat_dept.get().strip().upper()
        num = self.cat_num.get().strip()
        name = self.cat_name.get().strip()
        cred = self.cat_cred.get().strip()
        prereqs_str = self.cat_prereqs.get().strip()

        if not all([dept, num, name, cred]):
            messagebox.showwarning("Validation", "Department, Number, Name, and Credits are required.")
            return
        try:
            num = int(num)
            cred = int(cred)
        except ValueError:
            messagebox.showwarning("Validation", "Number and Credits must be integers.")
            return

        prereqs = [p.strip() for p in prereqs_str.split(",") if p.strip()] if prereqs_str else []
        course = Course(dept, num, name, cred, prereqs)
        self.uni.catalog.insert(course)
        self.uni._save()
        self._refresh_catalog_tree()
        self._set_status(f"Course '{name}' inserted into BST (O(log n)).")

        # Clear fields
        for e in [self.cat_dept, self.cat_num, self.cat_name, self.cat_cred, self.cat_prereqs]:
            e.delete(0, "end")

    def _delete_course(self):
        sel = self.catalog_tree.focus()
        if not sel:
            return
        name = self.catalog_tree.item(sel)["values"][2]
        if messagebox.askyesno("Confirm", f"Delete '{name}' from BST?"):
            self.uni.catalog.delete(name)
            self.uni._save()
            self._refresh_catalog_tree()
            self._set_status(f"Course '{name}' removed from BST.")

    def _refresh_catalog_tree(self):
        for item in self.catalog_tree.get_children():
            self.catalog_tree.delete(item)
        for i, c in enumerate(self.uni.catalog.inorder()):
            tag = "even" if i % 2 == 0 else "odd"
            prereqs_str = ", ".join(c.prereqs) if c.prereqs else "—"
            self.catalog_tree.insert("", "end", values=(c.dept, c.number, c.name, c.credits, prereqs_str), tags=(tag,))
        self.catalog_tree.tag_configure("even", background=TREEVIEW_BG)
        self.catalog_tree.tag_configure("odd", background=TREEVIEW_ALT)

    # ─── Offerings ───────────────────────────────────────────

    def _build_admin_offerings(self):
        parent = self.admin_offerings_tab

        form = ttk.LabelFrame(parent, text="  Schedule a Course Offering  ")
        form.pack(fill="x", padx=15, pady=(15, 5))

        fields = ttk.Frame(form, style="TFrame")
        fields.pack(fill="x", padx=15, pady=12)

        # Row 0 labels
        labels = ["Course (from BST)", "Section", "Year", "Quarter", "Capacity", "Time Slot"]
        for i, lbl in enumerate(labels):
            ttk.Label(fields, text=lbl, font=FONT_SMALL, foreground=TEXT_SECONDARY).grid(row=0, column=i, padx=6, sticky="w")

        catalog_names = [c.name for c in self.uni.catalog.inorder()]
        self.off_course = ttk.Combobox(fields, values=catalog_names, width=18, state="readonly")
        self.off_section = ttk.Entry(fields, width=5)
        self.off_section.insert(0, "1")
        self.off_year = ttk.Entry(fields, width=6)
        self.off_year.insert(0, "2026")
        self.off_quarter = ttk.Combobox(fields, values=["Fall", "Winter", "Spring", "Summer"], width=8, state="readonly")
        self.off_quarter.set("Spring")
        self.off_capacity = ttk.Entry(fields, width=5)
        self.off_capacity.insert(0, "30")
        self.off_time = ttk.Combobox(fields, values=[
            "MW 08:00-09:30", "MW 10:00-11:30", "MW 12:00-13:30", "MW 14:00-15:30",
            "TR 08:00-09:30", "TR 09:00-10:30", "TR 10:00-11:30", "TR 14:00-15:30",
        ], width=16)
        self.off_time.set("MW 10:00-11:30")

        widgets = [self.off_course, self.off_section, self.off_year, self.off_quarter, self.off_capacity, self.off_time]
        for i, w in enumerate(widgets):
            w.grid(row=1, column=i, padx=6, pady=(2, 0), sticky="ew")

        ttk.Button(fields, text="📅 Create Offering", style="Accent.TButton",
                   command=self._create_offering).grid(row=1, column=6, padx=(12, 0))

        # Offerings table
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        cols = ("id", "course", "section", "quarter", "time", "enrolled", "capacity", "waitlist")
        self.offer_tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        headings = [("id", "ID", 50), ("course", "Course", 180), ("section", "Sec", 50),
                    ("quarter", "Quarter", 90), ("time", "Time Slot", 140),
                    ("enrolled", "Enrolled", 80), ("capacity", "Cap", 50), ("waitlist", "Waitlist", 70)]
        for col, heading, w in headings:
            self.offer_tree.heading(col, text=heading)
            self.offer_tree.column(col, width=w, anchor="center")

        self.offer_tree.pack(fill="both", expand=True)
        self._refresh_offer_tree()

    def _create_offering(self):
        course_name = self.off_course.get()
        if not course_name:
            messagebox.showwarning("Validation", "Select a course from the BST catalog.")
            return
        course = self.uni.catalog.search(course_name)
        if not course:
            messagebox.showerror("Error", "Course not found in BST.")
            return
        try:
            section = int(self.off_section.get())
            year = int(self.off_year.get())
            capacity = int(self.off_capacity.get())
        except ValueError:
            messagebox.showwarning("Validation", "Section, Year, and Capacity must be numbers.")
            return

        offering = CourseOffering(course, section, year, self.off_quarter.get(), capacity, self.off_time.get())
        self.uni.offerings.append(offering)
        self.uni._save()
        self._refresh_offer_tree()
        self._set_status(f"Offering created: {offering.display_name} ({self.off_quarter.get()} {year})")

    def _refresh_offer_tree(self):
        for item in self.offer_tree.get_children():
            self.offer_tree.delete(item)
        for i, o in enumerate(self.uni.offerings):
            tag = "even" if i % 2 == 0 else "odd"
            self.offer_tree.insert("", "end", values=(
                i + 1, o.course.name, o.section, f"{o.quarter} {o.year}",
                o.time_slot, len(o.enrolled_students), o.capacity, len(o.waitlist)
            ), tags=(tag,))
        self.offer_tree.tag_configure("even", background=TREEVIEW_BG)
        self.offer_tree.tag_configure("odd", background=TREEVIEW_ALT)

    # ─── Students ────────────────────────────────────────────

    def _build_admin_students(self):
        parent = self.admin_students_tab

        # Toolbar
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill="x", padx=15, pady=(15, 5))

        ttk.Label(toolbar, text="🔍  Search:", font=FONT_BODY).pack(side="left")
        self.stu_search = ttk.Entry(toolbar, width=25)
        self.stu_search.pack(side="left", padx=8)
        self.stu_search.bind("<KeyRelease>", lambda e: self._refresh_student_tree())

        ttk.Button(toolbar, text="Sort by GPA ↓  (MergeSort)", style="Accent.TButton",
                   command=lambda: self._sort_students("gpa")).pack(side="right", padx=4)
        ttk.Button(toolbar, text="Sort by Last Name ↑", style="TButton",
                   command=lambda: self._sort_students("name")).pack(side="right", padx=4)

        # Add student form
        add_frame = ttk.LabelFrame(parent, text="  Add New Student  ")
        add_frame.pack(fill="x", padx=15, pady=5)
        add_inner = ttk.Frame(add_frame, style="TFrame")
        add_inner.pack(fill="x", padx=15, pady=10)

        for i, lbl in enumerate(["First Name", "Last Name", "Username", "DOB (YYYY-MM-DD)"]):
            ttk.Label(add_inner, text=lbl, font=FONT_SMALL, foreground=TEXT_SECONDARY).grid(row=0, column=i, padx=6, sticky="w")

        self.stu_first = ttk.Entry(add_inner, width=14)
        self.stu_last = ttk.Entry(add_inner, width=14)
        self.stu_user = ttk.Entry(add_inner, width=12)
        self.stu_dob = ttk.Entry(add_inner, width=14)
        for i, e in enumerate([self.stu_first, self.stu_last, self.stu_user, self.stu_dob]):
            e.grid(row=1, column=i, padx=6, pady=(2, 0), sticky="ew")

        ttk.Button(add_inner, text="➕ Add Student", style="Success.TButton",
                   command=self._add_student).grid(row=1, column=4, padx=(12, 0))

        # Table
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        cols = ("username", "name", "gpa", "completed", "active")
        self.student_tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        for col, heading, w in [("username", "Username", 100), ("name", "Full Name", 180),
                                 ("gpa", "GPA", 70), ("completed", "Completed", 80), ("active", "Active Courses", 200)]:
            self.student_tree.heading(col, text=heading)
            self.student_tree.column(col, width=w, anchor="center" if w < 120 else "w")
        self.student_tree.pack(fill="both", expand=True)

        self._refresh_student_tree()

    def _add_student(self):
        first = self.stu_first.get().strip()
        last = self.stu_last.get().strip()
        user = self.stu_user.get().strip()
        dob = self.stu_dob.get().strip()
        if not all([first, last, user, dob]):
            messagebox.showwarning("Validation", "All fields are required.")
            return
        if user in self.uni.students:
            messagebox.showwarning("Duplicate", f"Username '{user}' already exists.")
            return
        student = Student(first, last, user, dob)
        self.uni.students[user] = student
        self.uni._save()
        self._refresh_student_tree()
        self._set_status(f"Student '{first} {last}' added.")
        for e in [self.stu_first, self.stu_last, self.stu_user, self.stu_dob]:
            e.delete(0, "end")

    def _sort_students(self, by):
        from dsa_lib.sorting import merge_sort_students
        students = list(self.uni.students.values())
        if by == "gpa":
            sorted_list = merge_sort_students(students, key_func=lambda s: s.gpa, reverse=True)
            self._set_status("Students sorted by GPA (descending) using MergeSort O(n log n).")
        else:
            sorted_list = merge_sort_students(students, key_func=lambda s: s.last.lower(), reverse=False)
            self._set_status("Students sorted by Last Name (ascending) using MergeSort O(n log n).")
        self._populate_student_tree(sorted_list)
        messagebox.showinfo("DSA", f"Sorted {len(sorted_list)} students using custom MergeSort algorithm.")

    def _refresh_student_tree(self):
        query = self.stu_search.get().strip() if hasattr(self, "stu_search") else ""
        if query:
            results = self.uni.search_students(query)
            self._set_status(f"Linear Search: {len(results)} match(es) for '{query}'.")
        else:
            results = list(self.uni.students.values())
        self._populate_student_tree(results)

    def _populate_student_tree(self, students):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for i, s in enumerate(students):
            tag = "even" if i % 2 == 0 else "odd"
            active = ", ".join(s.active_schedule) if s.active_schedule else "—"
            self.student_tree.insert("", "end", values=(
                s.username, s.full_name, f"{s.gpa:.2f}", len(s.completed_courses), active
            ), tags=(tag,))
        self.student_tree.tag_configure("even", background=TREEVIEW_BG)
        self.student_tree.tag_configure("odd", background=TREEVIEW_ALT)

    # ─── Grades & Drop ───────────────────────────────────────

    def _build_admin_grades(self):
        parent = self.admin_grades_tab

        # ── Grade Entry Section ──
        grade_frame = ttk.LabelFrame(parent, text="  📝 Assign Grade  ")
        grade_frame.pack(fill="x", padx=15, pady=(15, 5))

        g_inner = ttk.Frame(grade_frame, style="TFrame")
        g_inner.pack(fill="x", padx=15, pady=12)

        ttk.Label(g_inner, text="Offering", font=FONT_SMALL, foreground=TEXT_SECONDARY).grid(row=0, column=0, padx=6, sticky="w")
        ttk.Label(g_inner, text="Student", font=FONT_SMALL, foreground=TEXT_SECONDARY).grid(row=0, column=1, padx=6, sticky="w")
        ttk.Label(g_inner, text="Grade", font=FONT_SMALL, foreground=TEXT_SECONDARY).grid(row=0, column=2, padx=6, sticky="w")

        offering_names = [f"{o.display_name} ({o.quarter} {o.year})" for o in self.uni.offerings]
        self.grade_offering = ttk.Combobox(g_inner, values=offering_names, width=25, state="readonly")
        self.grade_offering.grid(row=1, column=0, padx=6)
        self.grade_offering.bind("<<ComboboxSelected>>", self._on_grade_offering_change)

        self.grade_student = ttk.Combobox(g_inner, width=15, state="readonly")
        self.grade_student.grid(row=1, column=1, padx=6)

        self.grade_value = ttk.Combobox(g_inner, values=["A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-","F"],
                                         width=5, state="readonly")
        self.grade_value.grid(row=1, column=2, padx=6)

        ttk.Button(g_inner, text="✅ Assign Grade", style="Success.TButton",
                   command=self._assign_grade).grid(row=1, column=3, padx=(12, 0))

        # ── Drop Student Section ──
        drop_frame = ttk.LabelFrame(parent, text="  🚫 Drop Student from Offering  ")
        drop_frame.pack(fill="x", padx=15, pady=10)

        d_inner = ttk.Frame(drop_frame, style="TFrame")
        d_inner.pack(fill="x", padx=15, pady=12)

        ttk.Label(d_inner, text="Offering", font=FONT_SMALL, foreground=TEXT_SECONDARY).grid(row=0, column=0, padx=6, sticky="w")
        ttk.Label(d_inner, text="Enrolled Student", font=FONT_SMALL, foreground=TEXT_SECONDARY).grid(row=0, column=1, padx=6, sticky="w")

        self.drop_offering = ttk.Combobox(d_inner, values=offering_names, width=25, state="readonly")
        self.drop_offering.grid(row=1, column=0, padx=6)
        self.drop_offering.bind("<<ComboboxSelected>>", self._on_drop_offering_change)

        self.drop_student = ttk.Combobox(d_inner, width=15, state="readonly")
        self.drop_student.grid(row=1, column=1, padx=6)

        ttk.Button(d_inner, text="🚫 Drop & Auto-Dequeue", style="Danger.TButton",
                   command=self._drop_student).grid(row=1, column=2, padx=(12, 0))

        # ── Enrollment Info ──
        info_frame = ttk.LabelFrame(parent, text="  📋 Offering Enrollment Details  ")
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)

        cols = ("student", "status", "grade")
        self.enroll_tree = ttk.Treeview(info_frame, columns=cols, show="headings")
        for col, heading, w in [("student", "Student", 180), ("status", "Status", 120), ("grade", "Grade", 80)]:
            self.enroll_tree.heading(col, text=heading)
            self.enroll_tree.column(col, width=w, anchor="center")
        self.enroll_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def _on_grade_offering_change(self, event=None):
        idx = self.grade_offering.current()
        if idx < 0 or idx >= len(self.uni.offerings):
            return
        offering = self.uni.offerings[idx]
        self.grade_student.config(values=offering.enrolled_students)
        self._refresh_enroll_tree(offering)

    def _on_drop_offering_change(self, event=None):
        idx = self.drop_offering.current()
        if idx < 0 or idx >= len(self.uni.offerings):
            return
        offering = self.uni.offerings[idx]
        self.drop_student.config(values=offering.enrolled_students)
        self._refresh_enroll_tree(offering)

    def _refresh_enroll_tree(self, offering):
        for item in self.enroll_tree.get_children():
            self.enroll_tree.delete(item)
        for i, u in enumerate(offering.enrolled_students):
            grade = offering.grades.get(u, "—")
            tag = "even" if i % 2 == 0 else "odd"
            self.enroll_tree.insert("", "end", values=(u, "Enrolled", grade), tags=(tag,))
        for i, u in enumerate(offering.waitlist.to_list()):
            tag = "waitlist"
            self.enroll_tree.insert("", "end", values=(u, f"Waitlist #{i+1}", "—"), tags=(tag,))
        self.enroll_tree.tag_configure("even", background=TREEVIEW_BG)
        self.enroll_tree.tag_configure("odd", background=TREEVIEW_ALT)
        self.enroll_tree.tag_configure("waitlist", background="#fef3c7", foreground="#92400e")

    def _assign_grade(self):
        idx = self.grade_offering.current()
        student = self.grade_student.get()
        grade = self.grade_value.get()
        if idx < 0 or not student or not grade:
            messagebox.showwarning("Validation", "Select offering, student, and grade.")
            return
        offering = self.uni.offerings[idx]
        result = self.uni.finalize_grade(student, offering, grade)
        messagebox.showinfo("Grade Entry", result)
        self._refresh_enroll_tree(offering)
        self._refresh_student_tree()
        self._set_status(result)

    def _drop_student(self):
        idx = self.drop_offering.current()
        student = self.drop_student_combo_get()
        if idx < 0 or not student:
            messagebox.showwarning("Validation", "Select offering and student.")
            return
        offering = self.uni.offerings[idx]
        result = self.uni.drop_student(student, offering)
        messagebox.showinfo("Drop Student", result)
        # Refresh
        self._on_drop_offering_change()
        self._on_grade_offering_change()
        self._refresh_student_tree()
        self._refresh_offer_tree()
        self._set_status(result)

    def drop_student_combo_get(self):
        return self.drop_student.get()

    # ═══════════════════════════════════════════════════════════
    #  STUDENT TAB
    # ═══════════════════════════════════════════════════════════

    def _build_student_tab(self):
        # ── Top: Student Selector ──
        top = ttk.Frame(self.tab_student, style="Surface.TFrame")
        top.pack(fill="x", padx=15, pady=(15, 5))

        ttk.Label(top, text="👤  Active Student:", font=FONT_SUBTITLE,
                  style="Surface.TLabel").pack(side="left", padx=(10, 5))

        usernames = list(self.uni.students.keys())
        self.active_student = ttk.Combobox(top, values=usernames, width=15, state="readonly")
        self.active_student.pack(side="left", padx=5)
        if usernames:
            self.active_student.set(usernames[0])
        self.active_student.bind("<<ComboboxSelected>>", lambda e: self._refresh_student_portal())

        ttk.Button(top, text="🔄 Refresh", style="TButton",
                   command=self._refresh_student_portal).pack(side="left", padx=10)

        # ── Profile Card ──
        self.profile_frame = ttk.Frame(self.tab_student, style="Card.TFrame")
        self.profile_frame.pack(fill="x", padx=15, pady=10)

        # ── Student Inner Tabs ──
        stu_nb = ttk.Notebook(self.tab_student, style="Inner.TNotebook")
        stu_nb.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.stu_transcript_tab = ttk.Frame(stu_nb, style="TFrame")
        self.stu_register_tab = ttk.Frame(stu_nb, style="TFrame")
        self.stu_schedule_tab = ttk.Frame(stu_nb, style="TFrame")

        stu_nb.add(self.stu_transcript_tab, text=" 📜 Transcript ")
        stu_nb.add(self.stu_register_tab, text=" 📝 Register for Courses ")
        stu_nb.add(self.stu_schedule_tab, text=" 📅 My Schedule ")

        self._build_transcript_view()
        self._build_register_view()
        self._build_schedule_view()
        self._refresh_student_portal()

    def _refresh_student_portal(self):
        username = self.active_student.get()
        student = self.uni.students.get(username)
        if not student:
            return

        # Update profile card
        for w in self.profile_frame.winfo_children():
            w.destroy()

        inner = ttk.Frame(self.profile_frame, style="Card.TFrame")
        inner.pack(fill="x", padx=20, pady=14)

        # Avatar placeholder
        ttk.Label(inner, text="👤", font=(FONT_FAMILY, 36), style="Card.TLabel").pack(side="left", padx=(0, 16))

        info = ttk.Frame(inner, style="Card.TFrame")
        info.pack(side="left", fill="x", expand=True)
        ttk.Label(info, text=student.full_name, font=(FONT_FAMILY, 16, "bold"),
                  foreground=TEXT_PRIMARY, style="Card.TLabel").pack(anchor="w")
        ttk.Label(info, text=f"@{student.username}  ·  DOB: {student.dob}",
                  style="Dim.TLabel").pack(anchor="w", pady=(2, 0))

        # GPA badge
        gpa_frame = ttk.Frame(inner, style="Card.TFrame")
        gpa_frame.pack(side="right", padx=16)
        gpa_color = SUCCESS if student.gpa >= 3.5 else (WARNING if student.gpa >= 2.5 else DANGER)
        ttk.Label(gpa_frame, text=f"{student.gpa:.2f}", font=(FONT_FAMILY, 28, "bold"),
                  foreground=gpa_color, background=BG_CARD).pack()
        ttk.Label(gpa_frame, text="GPA", font=FONT_SMALL, foreground=TEXT_DIM,
                  background=BG_CARD).pack()

        # Stats
        stats_frame = ttk.Frame(inner, style="Card.TFrame")
        stats_frame.pack(side="right", padx=16)
        ttk.Label(stats_frame, text=str(len(student.completed_courses)), font=(FONT_FAMILY, 18, "bold"),
                  foreground=ACCENT, background=BG_CARD).pack()
        ttk.Label(stats_frame, text="Completed", font=FONT_SMALL, foreground=TEXT_DIM,
                  background=BG_CARD).pack()

        active_frame = ttk.Frame(inner, style="Card.TFrame")
        active_frame.pack(side="right", padx=16)
        ttk.Label(active_frame, text=str(len(student.active_schedule)), font=(FONT_FAMILY, 18, "bold"),
                  foreground=WARNING, background=BG_CARD).pack()
        ttk.Label(active_frame, text="Active", font=FONT_SMALL, foreground=TEXT_DIM,
                  background=BG_CARD).pack()

        self._refresh_transcript()
        self._refresh_register_view()
        self._refresh_schedule_view()

    # ─── Transcript ──────────────────────────────────────────

    def _build_transcript_view(self):
        parent = self.stu_transcript_tab

        cols = ("course", "grade", "points")
        self.transcript_tree = ttk.Treeview(parent, columns=cols, show="headings")
        for col, heading, w in [("course", "Course Name", 280), ("grade", "Grade", 80), ("points", "Quality Points", 120)]:
            self.transcript_tree.heading(col, text=heading)
            self.transcript_tree.column(col, width=w, anchor="center")
        self.transcript_tree.pack(fill="both", expand=True, padx=15, pady=15)

    def _refresh_transcript(self):
        for item in self.transcript_tree.get_children():
            self.transcript_tree.delete(item)
        username = self.active_student.get()
        student = self.uni.students.get(username)
        if not student:
            return
        scale = {"A+":4.0,"A":4.0,"A-":3.7,"B+":3.3,"B":3.0,"B-":2.7,
                 "C+":2.3,"C":2.0,"C-":1.7,"D+":1.3,"D":1.0,"D-":0.7,"F":0.0}
        for i, (course, grade) in enumerate(student.completed_courses.items()):
            pts = scale.get(grade, 0.0)
            tag = "even" if i % 2 == 0 else "odd"
            self.transcript_tree.insert("", "end", values=(course, grade, f"{pts:.1f}"), tags=(tag,))
        self.transcript_tree.tag_configure("even", background=TREEVIEW_BG)
        self.transcript_tree.tag_configure("odd", background=TREEVIEW_ALT)

    # ─── Registration ────────────────────────────────────────

    def _build_register_view(self):
        parent = self.stu_register_tab

        # Available offerings
        cols = ("id", "course", "time", "seats", "waitlist", "status")
        self.reg_tree = ttk.Treeview(parent, columns=cols, show="headings", selectmode="browse")
        for col, heading, w in [("id", "#", 40), ("course", "Course", 200), ("time", "Time Slot", 150),
                                 ("seats", "Seats Left", 90), ("waitlist", "Waitlist", 70), ("status", "Your Status", 120)]:
            self.reg_tree.heading(col, text=heading)
            self.reg_tree.column(col, width=w, anchor="center")
        self.reg_tree.pack(fill="both", expand=True, padx=15, pady=(15, 5))

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", padx=15, pady=(5, 15))
        ttk.Button(btn_frame, text="📝  Request Enrollment", style="Accent.TButton",
                   command=self._request_enrollment).pack(side="left")
        self.reg_status_label = ttk.Label(btn_frame, text="", font=FONT_BODY, foreground=TEXT_SECONDARY)
        self.reg_status_label.pack(side="left", padx=15)

    def _refresh_register_view(self):
        for item in self.reg_tree.get_children():
            self.reg_tree.delete(item)
        username = self.active_student.get()
        student = self.uni.students.get(username)
        if not student:
            return

        for i, o in enumerate(self.uni.offerings):
            seats = o.seats_available
            wl = len(o.waitlist)
            # Determine user's status
            if username in o.enrolled_students:
                status = "✅ Enrolled"
            elif username in o.waitlist:
                pos = o.waitlist.position_of(username)
                status = f"⏳ Waitlist #{pos}"
            else:
                status = "Available" if not o.is_full else "Full"

            tag = "enrolled" if "Enrolled" in status else ("waitlist_row" if "Waitlist" in status else ("even" if i % 2 == 0 else "odd"))
            self.reg_tree.insert("", "end", values=(
                i + 1, f"{o.course.dept} {o.course.number}: {o.course.name}",
                o.time_slot, max(seats, 0), wl, status
            ), tags=(tag,))

        self.reg_tree.tag_configure("even", background=TREEVIEW_BG)
        self.reg_tree.tag_configure("odd", background=TREEVIEW_ALT)
        self.reg_tree.tag_configure("enrolled", background="#dcfce7", foreground="#166534")
        self.reg_tree.tag_configure("waitlist_row", background="#fef3c7", foreground="#92400e")

    def _request_enrollment(self):
        sel = self.reg_tree.focus()
        if not sel:
            messagebox.showwarning("Selection", "Please select a course offering.")
            return
        vals = self.reg_tree.item(sel)["values"]
        idx = int(vals[0]) - 1
        if idx < 0 or idx >= len(self.uni.offerings):
            return

        offering = self.uni.offerings[idx]
        username = self.active_student.get()

        result = self.uni.register_student(username, offering)

        if "SUCCESS" in result:
            messagebox.showinfo("Enrollment", result)
        elif "WAITLIST" in result:
            messagebox.showinfo("Waitlist (FCFS Queue)", result)
        else:
            messagebox.showwarning("Registration Failed", result)

        self._refresh_student_portal()
        self._refresh_offer_tree()
        self.reg_status_label.config(text=result)
        self._set_status(result)

    # ─── Schedule ────────────────────────────────────────────

    def _build_schedule_view(self):
        parent = self.stu_schedule_tab

        cols = ("course", "section", "time", "quarter")
        self.schedule_tree = ttk.Treeview(parent, columns=cols, show="headings")
        for col, heading, w in [("course", "Course", 250), ("section", "Section", 70),
                                 ("time", "Time Slot", 150), ("quarter", "Quarter", 120)]:
            self.schedule_tree.heading(col, text=heading)
            self.schedule_tree.column(col, width=w, anchor="center")
        self.schedule_tree.pack(fill="both", expand=True, padx=15, pady=15)

    def _refresh_schedule_view(self):
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        username = self.active_student.get()
        student = self.uni.students.get(username)
        if not student:
            return
        for i, offering_name in enumerate(student.active_schedule):
            # Find the matching offering
            for o in self.uni.offerings:
                if o.display_name == offering_name:
                    tag = "even" if i % 2 == 0 else "odd"
                    self.schedule_tree.insert("", "end", values=(
                        o.course.name, o.section, o.time_slot, f"{o.quarter} {o.year}"
                    ), tags=(tag,))
                    break
        self.schedule_tree.tag_configure("even", background=TREEVIEW_BG)
        self.schedule_tree.tag_configure("odd", background=TREEVIEW_ALT)


# ═══════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityApp(root)
    root.mainloop()