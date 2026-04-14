"""
University Registration System — Modern Tkinter Desktop App
Uses custom DSA structures: BST (catalog), LinkedQueue (waitlists), MergeSort, Linear Search.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from registrar import Institution, Course, CourseOffering, Student, Admin, hash_password, GPA_SCALE
from utils.image_processing import process_avatar, save_avatar_file

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
        
        self.current_user = None
        self.current_role = None
        
        self.main_container = ttk.Frame(self.root, style="TFrame")
        self.main_container.pack(fill="both", expand=True)

        self.show_login()

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def logout(self):
        self.current_user = None
        self.current_role = None
        self.show_login()

    def show_login(self):
        self.clear_container()
        from auth_views import LoginFrame
        LoginFrame(self.main_container, self).pack(fill="both", expand=True)

    def show_register(self):
        self.clear_container()
        from auth_views import RegisterFrame
        RegisterFrame(self.main_container, self).pack(fill="both", expand=True)

    def login_action(self, username, pwd, role):
        if not username or not pwd:
            messagebox.showwarning("Login Failed", "Username and password required.")
            return

        user_dict = self.uni.students if role == "Student" else self.uni.admins
        user = user_dict.get(username)
        
        # Also check email
        if not user:
            for u in user_dict.values():
                if u.email == username:
                    user = u
                    break

        if not user:
            messagebox.showerror("Login Failed", "User not found.")
            return

        if user.password_hash != hash_password(pwd):
            messagebox.showerror("Login Failed", "Incorrect password.")
            return

        self.current_user = user
        self.current_role = role
        self.show_dashboard()

    def register_action(self, first, last, username, dob, email, pwd, role, avatar_path):
        from registrar import Student, Admin, hash_password
        
        user_dict = self.uni.students if role == "Student" else self.uni.admins
        if username in user_dict:
            return False, f"Username '{username}' already exists."
            
        for u in user_dict.values():
            if u.email == email:
                return False, f"Email '{email}' already exists."
                
        saved_avatar_path = ""
        if avatar_path:
            from utils.image_processing import save_avatar_file
            saved_avatar_path = save_avatar_file(avatar_path, username)

        if role == "Student":
            new_user = Student(first, last, username, dob, email, hash_password(pwd), saved_avatar_path)
            self.uni.students[username] = new_user
        else:
            new_user = Admin(first, last, username, email, hash_password(pwd), saved_avatar_path)
            self.uni.admins[username] = new_user
            
        self.uni._save()
        return True, "Registration successful. Please log in."

    def show_dashboard(self):
        self.clear_container()
        self._build_header()

        # Content area — no outer notebook wrapper, just straight into the role view
        self.content_frame = ttk.Frame(self.main_container, style="TFrame")
        self.content_frame.pack(expand=True, fill="both", padx=0, pady=0)

        if self.current_role == "Admin":
            self.tab_admin = self.content_frame
            self._build_admin_tab()
        else:
            self.tab_student = self.content_frame
            self._build_student_tab()

        self._build_status_bar()

    # ═══════════════════════════════════════════════════════════
    #  HEADER
    # ═══════════════════════════════════════════════════════════

    def _build_header(self):
        header = ttk.Frame(self.main_container, style="Surface.TFrame")
        header.pack(fill="x", padx=0, pady=0)

        inner = ttk.Frame(header, style="Surface.TFrame")
        inner.pack(fill="x", padx=30, pady=(16, 12))

        avatar_path = getattr(self.current_user, 'avatar_path', "")
        from utils.image_processing import process_avatar
        self.header_avatar_img = process_avatar(avatar_path, size=(50, 50))
        
        if self.header_avatar_img:
            ttk.Label(inner, image=self.header_avatar_img, style="Surface.TLabel").pack(side="left", padx=(0, 15))
        else:
            ttk.Label(inner, text="👤", font=(FONT_FAMILY, 28), style="Surface.TLabel").pack(side="left", padx=(0, 15))

        text_block = ttk.Frame(inner, style="Surface.TFrame")
        text_block.pack(side="left")
        
        welcome_text = f"Welcome, {self.current_user.full_name} ({self.current_role})"
        ttk.Label(text_block, text=welcome_text, font=(FONT_FAMILY, 15, "bold"),
                  foreground=TEXT_PRIMARY, style="Surface.TLabel").pack(anchor="w")
        ttk.Label(text_block, text=f"{self.uni.name}  ·  Academic Management System",
                  font=FONT_SMALL, foreground=TEXT_DIM, style="Surface.TLabel").pack(anchor="w")

        # Stats on the right
        stats = ttk.Frame(inner, style="Surface.TFrame")
        stats.pack(side="right")
        
        if self.current_role == "Admin":
            self._header_stat_labels = {}
            n_courses  = len(self.uni.catalog)
            n_students  = len(self.uni.students)
            n_offerings = len(self.uni.offerings)
            for key, label, val, color in [
                ("courses",  "Courses",  n_courses,  ACCENT),
                ("students", "Students", n_students, SUCCESS),
                ("offerings","Offerings",n_offerings, WARNING)
            ]:
                chip = ttk.Frame(stats, style="Surface.TFrame")
                chip.pack(side="left", padx=12)
                lbl_val = ttk.Label(chip, text=str(val), font=(FONT_FAMILY, 16, "bold"),
                          foreground=color, style="Surface.TLabel")
                lbl_val.pack()
                self._header_stat_labels[key] = lbl_val
                ttk.Label(chip, text=label, font=FONT_SMALL,
                          foreground=TEXT_DIM, style="Surface.TLabel").pack()
                      
        # Add Logout Button inside header stats
        logout_chip = ttk.Frame(stats, style="Surface.TFrame")
        logout_chip.pack(side="left", padx=(30, 0))
        ttk.Button(logout_chip, text="🚪 Sign Out", style="Danger.TButton",
                   command=self.logout).pack(pady=4)

    def _refresh_header_stats(self):
        """Update the live stat counters in the admin header."""
        if not hasattr(self, '_header_stat_labels'):
            return
        labels = self._header_stat_labels
        if "courses" in labels:
            labels["courses"].config(text=str(len(self.uni.catalog)))
        if "students" in labels:
            labels["students"].config(text=str(len(self.uni.students)))
        if "offerings" in labels:
            labels["offerings"].config(text=str(len(self.uni.offerings)))

    # ═══════════════════════════════════════════════════════════
    #  MAIN NOTEBOOK
    # ═══════════════════════════════════════════════════════════

    def _build_status_bar(self):
        bar = ttk.Frame(self.main_container, style="Surface.TFrame")
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
        parent = self.tab_admin

        # ── Two-pane layout: left sidebar nav + right content ──
        sidebar = tk.Frame(parent, bg=ACCENT, width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self.admin_content = ttk.Frame(parent, style="TFrame")
        self.admin_content.pack(side="left", fill="both", expand=True)

        # Sidebar nav items
        tk.Label(sidebar, text="⚙  Admin", bg=ACCENT, fg="#ffffff",
                 font=(FONT_FAMILY, 13, "bold"), pady=20).pack(fill="x")
        tk.Frame(sidebar, bg="#6366f1", height=1).pack(fill="x", padx=16)

        self._admin_nav_btns = {}
        nav_items = [
            ("catalog",   "📚  Course Catalog"),
            ("offerings", "📅  Offerings"),
            ("students",  "👥  Students"),
            ("grades",    "📝  Grades & Drop"),
        ]
        for key, label in nav_items:
            btn = tk.Label(sidebar, text=label, bg=ACCENT, fg="#c7d2fe",
                           font=(FONT_FAMILY, 10), anchor="w", padx=22, pady=13,
                           cursor="hand2")
            btn.pack(fill="x")
            btn.bind("<Button-1>", lambda e, k=key: self._show_admin_section(k))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=ACCENT_HOVER, fg="#ffffff"))
            btn.bind("<Leave>", lambda e, b=btn, k2=key: b.config(
                bg="#3730a3" if self._admin_active == k2 else ACCENT,
                fg="#ffffff" if self._admin_active == k2 else "#c7d2fe"))
            self._admin_nav_btns[key] = btn

        # Pre-build all section frames (hidden)
        self.admin_catalog_tab    = ttk.Frame(self.admin_content, style="TFrame")
        self.admin_offerings_tab  = ttk.Frame(self.admin_content, style="TFrame")
        self.admin_students_tab   = ttk.Frame(self.admin_content, style="TFrame")
        self.admin_grades_tab     = ttk.Frame(self.admin_content, style="TFrame")

        self._build_admin_catalog()
        self._build_admin_offerings()
        self._build_admin_students()
        self._build_admin_grades()

        self._admin_active = "catalog"
        self._show_admin_section("catalog")

    def _show_admin_section(self, key):
        self._admin_active = key
        section_map = {
            "catalog":   self.admin_catalog_tab,
            "offerings": self.admin_offerings_tab,
            "students":  self.admin_students_tab,
            "grades":    self.admin_grades_tab,
        }
        for k, frame in section_map.items():
            frame.pack_forget()
        section_map[key].pack(fill="both", expand=True)

        # Update highlight
        for k, btn in self._admin_nav_btns.items():
            if k == key:
                btn.config(bg="#3730a3", fg="#ffffff")
            else:
                btn.config(bg=ACCENT, fg="#c7d2fe")

    # ─── Catalog ─────────────────────────────────────────────

    def _build_admin_catalog(self):
        parent = self.admin_catalog_tab

        # ── Section header ──
        hdr = ttk.Frame(parent, style="Surface.TFrame")
        hdr.pack(fill="x", padx=0, pady=0)
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=16)
        ttk.Label(hdr_inner, text="Course Catalog", font=(FONT_FAMILY, 16, "bold"),
                  foreground=TEXT_PRIMARY, style="Surface.TLabel").pack(side="left")
        ttk.Label(hdr_inner, text="BST — sorted in-order", font=FONT_SMALL,
                  foreground=TEXT_DIM, style="Surface.TLabel").pack(side="left", padx=12)
        ttk.Button(hdr_inner, text="🗑  Delete Selected", style="Danger.TButton",
                   command=self._delete_course).pack(side="right")
        ttk.Separator(parent, orient="horizontal").pack(fill="x")

        # ── Add form card ──
        card = ttk.Frame(parent, style="Surface.TFrame")
        card.pack(fill="x", padx=20, pady=16)
        ttk.Label(card, text="Add Course", font=(FONT_FAMILY, 10, "bold"),
                  foreground=ACCENT, style="Surface.TLabel").pack(anchor="w", pady=(0, 8))

        fields = ttk.Frame(card, style="Surface.TFrame")
        fields.pack(fill="x")
        field_defs = [("Dept", 6), ("#", 5), ("Course Name", 22), ("Credits", 5), ("Prerequisites (comma-sep)", 26)]
        for i, (lbl, _) in enumerate(field_defs):
            ttk.Label(fields, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel").grid(row=0, column=i, padx=5, sticky="w")
        self.cat_dept = ttk.Entry(fields, width=field_defs[0][1])
        self.cat_num = ttk.Entry(fields, width=field_defs[1][1])
        self.cat_name = ttk.Entry(fields, width=field_defs[2][1])
        self.cat_cred = ttk.Entry(fields, width=field_defs[3][1])
        self.cat_prereqs = ttk.Entry(fields, width=field_defs[4][1])
        for i, e in enumerate([self.cat_dept, self.cat_num, self.cat_name, self.cat_cred, self.cat_prereqs]):
            e.grid(row=1, column=i, padx=5, pady=(4, 0), sticky="ew")
        ttk.Button(fields, text="➕ Add Course", style="Accent.TButton",
                   command=self._add_course).grid(row=1, column=5, padx=(12, 0))

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=20)

        # ── Table ──
        tree_wrap = ttk.Frame(parent, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("dept", "number", "name", "credits", "prereqs")
        self.catalog_tree = ttk.Treeview(tree_wrap, columns=cols, show="headings", selectmode="browse")
        for col, heading, w, anchor in [
            ("dept", "Dept", 70, "center"), ("number", "#", 60, "center"),
            ("name", "Course Name", 230, "w"), ("credits", "Cr", 50, "center"),
            ("prereqs", "Prerequisites", 0, "w")]:
            self.catalog_tree.heading(col, text=heading)
            self.catalog_tree.column(col, width=w, anchor=anchor, stretch=(col=="prereqs"))
        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.catalog_tree.yview)
        self.catalog_tree.configure(yscrollcommand=vsb.set)
        self.catalog_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
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
        self._refresh_header_stats()
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
            self._refresh_header_stats()
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

        # ── Section header ──
        hdr = ttk.Frame(parent, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=16)
        ttk.Label(hdr_inner, text="Course Offerings", font=(FONT_FAMILY, 16, "bold"),
                  foreground=TEXT_PRIMARY, style="Surface.TLabel").pack(side="left")
        ttk.Label(hdr_inner, text="Scheduled sections & enrollment", font=FONT_SMALL,
                  foreground=TEXT_DIM, style="Surface.TLabel").pack(side="left", padx=12)
        ttk.Separator(parent, orient="horizontal").pack(fill="x")

        # ── Create offering card ──
        card = ttk.Frame(parent, style="Surface.TFrame")
        card.pack(fill="x", padx=20, pady=16)
        ttk.Label(card, text="Schedule New Offering", font=(FONT_FAMILY, 10, "bold"),
                  foreground=ACCENT, style="Surface.TLabel").pack(anchor="w", pady=(0, 8))

        fields = ttk.Frame(card, style="Surface.TFrame")
        fields.pack(fill="x")
        labels = ["Course (BST)", "Section", "Year", "Quarter", "Capacity", "Time Slot"]
        for i, lbl in enumerate(labels):
            ttk.Label(fields, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel").grid(row=0, column=i, padx=5, sticky="w")
        catalog_names = [c.name for c in self.uni.catalog.inorder()]
        self.off_course = ttk.Combobox(fields, values=catalog_names, width=20, state="readonly")
        self.off_section = ttk.Entry(fields, width=5); self.off_section.insert(0, "1")
        self.off_year = ttk.Entry(fields, width=6); self.off_year.insert(0, "2026")
        self.off_quarter = ttk.Combobox(fields, values=["Fall","Winter","Spring","Summer"], width=8, state="readonly")
        self.off_quarter.set("Spring")
        self.off_capacity = ttk.Entry(fields, width=5); self.off_capacity.insert(0, "30")
        self.off_time = ttk.Combobox(fields, values=[
            "MW 08:00-09:30","MW 10:00-11:30","MW 12:00-13:30","MW 14:00-15:30",
            "TR 08:00-09:30","TR 09:00-10:30","TR 10:00-11:30","TR 14:00-15:30",
        ], width=16)
        self.off_time.set("MW 10:00-11:30")
        for i, w in enumerate([self.off_course, self.off_section, self.off_year,
                                self.off_quarter, self.off_capacity, self.off_time]):
            w.grid(row=1, column=i, padx=5, pady=(4, 0), sticky="ew")
        ttk.Button(fields, text="📅 Create", style="Accent.TButton",
                   command=self._create_offering).grid(row=1, column=6, padx=(12, 0))

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=20)

        # ── Offerings table ──
        tree_wrap = ttk.Frame(parent, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("id", "course", "section", "quarter", "time", "enrolled", "capacity", "waitlist")
        self.offer_tree = ttk.Treeview(tree_wrap, columns=cols, show="headings", selectmode="browse")
        for col, heading, w in [("id","#",40),("course","Course",190),("section","Sec",50),
                                 ("quarter","Quarter",95),("time","Time Slot",140),
                                 ("enrolled","Enrolled",75),("capacity","Cap",55),("waitlist","Waitlist",65)]:
            self.offer_tree.heading(col, text=heading)
            self.offer_tree.column(col, width=w, anchor="center")
        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.offer_tree.yview)
        self.offer_tree.configure(yscrollcommand=vsb.set)
        self.offer_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
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
        self._refresh_header_stats()
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

        # ── Section header ──
        hdr = ttk.Frame(parent, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=16)
        ttk.Label(hdr_inner, text="Students", font=(FONT_FAMILY, 16, "bold"),
                  foreground=TEXT_PRIMARY, style="Surface.TLabel").pack(side="left")

        sort_frame = ttk.Frame(hdr_inner, style="Surface.TFrame")
        sort_frame.pack(side="right")
        ttk.Button(sort_frame, text="Sort by GPA ↓", style="Accent.TButton",
                   command=lambda: self._sort_students("gpa")).pack(side="left", padx=4)
        ttk.Button(sort_frame, text="Sort by Name ↑", style="TButton",
                   command=lambda: self._sort_students("name")).pack(side="left", padx=4)
        ttk.Separator(parent, orient="horizontal").pack(fill="x")

        # ── Search bar ──
        search_bar = ttk.Frame(parent, style="Surface.TFrame")
        search_bar.pack(fill="x", padx=20, pady=12)
        ttk.Label(search_bar, text="🔍", font=(FONT_FAMILY, 11),
                  style="Surface.TLabel").pack(side="left", padx=(0, 6))
        self.stu_search = ttk.Entry(search_bar, width=30, font=(FONT_FAMILY, 10))
        self.stu_search.pack(side="left")
        self.stu_search.bind("<KeyRelease>", lambda e: self._refresh_student_tree())

        # ── Add student card ──
        card = ttk.Frame(parent, style="Surface.TFrame")
        card.pack(fill="x", padx=20, pady=(0, 12))
        ttk.Label(card, text="Add Student", font=(FONT_FAMILY, 10, "bold"),
                  foreground=ACCENT, style="Surface.TLabel").pack(anchor="w", pady=(0, 6))
        fields = ttk.Frame(card, style="Surface.TFrame")
        fields.pack(fill="x")
        for i, lbl in enumerate(["First Name", "Last Name", "Username", "DOB (YYYY-MM-DD)"]):
            ttk.Label(fields, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel").grid(row=0, column=i, padx=5, sticky="w")
        self.stu_first = ttk.Entry(fields, width=13)
        self.stu_last  = ttk.Entry(fields, width=13)
        self.stu_user  = ttk.Entry(fields, width=12)
        self.stu_dob   = ttk.Entry(fields, width=13)
        for i, e in enumerate([self.stu_first, self.stu_last, self.stu_user, self.stu_dob]):
            e.grid(row=1, column=i, padx=5, pady=(4, 0), sticky="ew")
        ttk.Button(fields, text="➕ Add", style="Success.TButton",
                   command=self._add_student).grid(row=1, column=4, padx=(12, 0))

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=20)

        # ── Table ──
        tree_wrap = ttk.Frame(parent, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("username", "name", "gpa", "completed", "active")
        self.student_tree = ttk.Treeview(tree_wrap, columns=cols, show="headings", selectmode="browse")
        for col, heading, w, anchor in [
            ("username","Username",100,"center"),("name","Full Name",190,"w"),
            ("gpa","GPA",65,"center"),("completed","Completed",85,"center"),("active","Active Courses",0,"w")]:
            self.student_tree.heading(col, text=heading)
            self.student_tree.column(col, width=w, anchor=anchor, stretch=(col=="active"))
        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=vsb.set)
        self.student_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
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
        self._refresh_header_stats()
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
        offering_names = [f"{o.display_name} ({o.quarter} {o.year})" for o in self.uni.offerings]

        # ── Section header ──
        hdr = ttk.Frame(parent, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=16)
        ttk.Label(hdr_inner, text="Grades & Enrollment", font=(FONT_FAMILY, 16, "bold"),
                  foreground=TEXT_PRIMARY, style="Surface.TLabel").pack(side="left")
        ttk.Separator(parent, orient="horizontal").pack(fill="x")

        # ── Two-column control area ──
        controls = ttk.Frame(parent, style="Surface.TFrame")
        controls.pack(fill="x", padx=20, pady=16)
        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)

        # Assign grade card (left)
        gc = ttk.Frame(controls, style="Surface.TFrame")
        gc.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ttk.Label(gc, text="Assign Grade", font=(FONT_FAMILY, 10, "bold"),
                  foreground=ACCENT, style="Surface.TLabel").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))
        for i, lbl in enumerate(["Offering", "Student", "Grade"]):
            ttk.Label(gc, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel").grid(row=1, column=i, padx=5, sticky="w")
        self.grade_offering = ttk.Combobox(gc, values=offering_names, width=22, state="readonly")
        self.grade_offering.grid(row=2, column=0, padx=5, pady=(4, 0), sticky="ew")
        self.grade_offering.bind("<<ComboboxSelected>>", self._on_grade_offering_change)
        self.grade_student = ttk.Combobox(gc, width=14, state="readonly")
        self.grade_student.grid(row=2, column=1, padx=5, pady=(4, 0))
        self.grade_value = ttk.Combobox(gc, values=["A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-","F"],
                                         width=5, state="readonly")
        self.grade_value.grid(row=2, column=2, padx=5, pady=(4, 0))
        ttk.Button(gc, text="✅ Assign", style="Success.TButton",
                   command=self._assign_grade).grid(row=2, column=3, padx=(10, 0), pady=(4, 0))

        # Drop student card (right)
        dc = ttk.Frame(controls, style="Surface.TFrame")
        dc.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ttk.Label(dc, text="Drop Student", font=(FONT_FAMILY, 10, "bold"),
                  foreground=DANGER, style="Surface.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))
        for i, lbl in enumerate(["Offering", "Student"]):
            ttk.Label(dc, text=lbl, font=(FONT_FAMILY, 8, "bold"),
                      foreground=TEXT_SECONDARY, style="Surface.TLabel").grid(row=1, column=i, padx=5, sticky="w")
        self.drop_offering = ttk.Combobox(dc, values=offering_names, width=22, state="readonly")
        self.drop_offering.grid(row=2, column=0, padx=5, pady=(4, 0), sticky="ew")
        self.drop_offering.bind("<<ComboboxSelected>>", self._on_drop_offering_change)
        self.drop_student = ttk.Combobox(dc, width=14, state="readonly")
        self.drop_student.grid(row=2, column=1, padx=5, pady=(4, 0))
        ttk.Button(dc, text="🚫 Drop", style="Danger.TButton",
                   command=self._drop_student).grid(row=2, column=2, padx=(10, 0), pady=(4, 0))

        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=20, pady=(4, 0))

        # ── Enrollment detail tree ──
        lbl_row = ttk.Frame(parent, style="TFrame")
        lbl_row.pack(fill="x", padx=24, pady=(12, 4))
        ttk.Label(lbl_row, text="Enrollment Details", font=(FONT_FAMILY, 10, "bold"),
                  foreground=TEXT_PRIMARY).pack(side="left")
        tree_wrap = ttk.Frame(parent, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        cols = ("student", "status", "grade")
        self.enroll_tree = ttk.Treeview(tree_wrap, columns=cols, show="headings")
        for col, heading, w in [("student","Student",200),("status","Status",130),("grade","Grade",80)]:
            self.enroll_tree.heading(col, text=heading)
            self.enroll_tree.column(col, width=w, anchor="center")
        vsb2 = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.enroll_tree.yview)
        self.enroll_tree.configure(yscrollcommand=vsb2.set)
        self.enroll_tree.pack(side="left", fill="both", expand=True)
        vsb2.pack(side="right", fill="y")

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
        student = self.drop_student.get()
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



    # ═══════════════════════════════════════════════════════════
    #  STUDENT TAB
    # ═══════════════════════════════════════════════════════════

    def _build_student_tab(self):
        parent = self.tab_student

        # ── Two-pane layout: left profile sidebar + right content ──
        # Profile sidebar
        self.stu_sidebar = tk.Frame(parent, bg=BG_CARD, width=220)
        self.stu_sidebar.pack(side="left", fill="y")
        self.stu_sidebar.pack_propagate(False)

        # Right content area with sub-navigation
        right = ttk.Frame(parent, style="TFrame")
        right.pack(side="left", fill="both", expand=True)

        # Right nav bar
        nav_bar = ttk.Frame(right, style="Surface.TFrame")
        nav_bar.pack(fill="x")
        ttk.Separator(right, orient="horizontal").pack(fill="x")

        self._stu_nav_btns = {}
        self._stu_active_section = "transcript"
        nav_items = [
            ("transcript", "📜  Transcript"),
            ("register",   "📝  Register"),
            ("schedule",   "📅  My Schedule"),
        ]
        for key, label in nav_items:
            btn = tk.Label(nav_bar, text=label, bg=BG_SURFACE, fg=TEXT_SECONDARY,
                           font=(FONT_FAMILY, 10), padx=20, pady=12, cursor="hand2")
            btn.pack(side="left")
            btn.bind("<Button-1>", lambda e, k=key: self._show_stu_section(k))
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=ACCENT) if b["bg"] == BG_SURFACE else None)
            btn.bind("<Leave>", lambda e, b=btn, k2=key:
                     b.config(fg=TEXT_SECONDARY if self._stu_active_section != k2 else ACCENT))
            self._stu_nav_btns[key] = btn

        # Content panels
        self.stu_transcript_tab = ttk.Frame(right, style="TFrame")
        self.stu_register_tab   = ttk.Frame(right, style="TFrame")
        self.stu_schedule_tab   = ttk.Frame(right, style="TFrame")

        self._build_transcript_view()
        self._build_register_view()
        self._build_schedule_view()
        self._refresh_student_portal()
        self._show_stu_section("transcript")

    def _show_stu_section(self, key):
        self._stu_active_section = key
        section_map = {
            "transcript": self.stu_transcript_tab,
            "register":   self.stu_register_tab,
            "schedule":   self.stu_schedule_tab,
        }
        for frame in section_map.values():
            frame.pack_forget()
        section_map[key].pack(fill="both", expand=True)

        # Lazily refresh only the section being navigated to so we never
        # do redundant work rebuilding hidden views.
        refresh_map = {
            "transcript": self._refresh_transcript,
            "register":   self._refresh_register_view,
            "schedule":   self._refresh_schedule_view,
        }
        refresh_map[key]()

        for k, btn in self._stu_nav_btns.items():
            if k == key:
                btn.config(fg=ACCENT, font=(FONT_FAMILY, 10, "bold"),
                           relief="flat", bd=0)
            else:
                btn.config(fg=TEXT_SECONDARY, font=(FONT_FAMILY, 10),
                           relief="flat", bd=0)

    def _refresh_student_portal(self):
        username = self.current_user.username
        student = self.uni.students.get(username)
        if not student:
            return

        # Clear and rebuild sidebar
        for w in self.stu_sidebar.winfo_children():
            w.destroy()

        # Avatar
        avatar_frame = tk.Frame(self.stu_sidebar, bg=BG_CARD)
        avatar_frame.pack(fill="x", pady=(28, 0))
        from utils.image_processing import process_avatar
        self.profile_avatar_img = process_avatar(getattr(student, 'avatar_path', ''), size=(88, 88))
        if self.profile_avatar_img:
            av_lbl = tk.Label(avatar_frame, image=self.profile_avatar_img, bg=BG_CARD)
        else:
            av_lbl = tk.Label(avatar_frame, text="👤", font=(FONT_FAMILY, 42), bg=BG_CARD)
        av_lbl.pack()

        # Name & username
        tk.Label(self.stu_sidebar, text=student.full_name, bg=BG_CARD,
                 fg=TEXT_PRIMARY, font=(FONT_FAMILY, 12, "bold"),
                 wraplength=190, justify="center").pack(pady=(10, 2))
        tk.Label(self.stu_sidebar, text=f"@{student.username}", bg=BG_CARD,
                 fg=TEXT_DIM, font=(FONT_FAMILY, 9)).pack()

        # Age
        try:
            from datetime import datetime
            dob_dt = datetime.strptime(student.dob, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - dob_dt.year - ((today.month, today.day) < (dob_dt.month, dob_dt.day))
            age_str = f"Age {age}"
        except:
            age_str = ""
        if age_str:
            tk.Label(self.stu_sidebar, text=age_str, bg=BG_CARD,
                     fg=TEXT_DIM, font=(FONT_FAMILY, 9)).pack(pady=(2, 0))

        # Divider
        tk.Frame(self.stu_sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=18)

        # Stats
        gpa_color = SUCCESS if student.gpa >= 3.5 else (WARNING if student.gpa >= 2.5 else DANGER)
        stats = [
            (f"{student.gpa:.2f}", "GPA",       gpa_color),
            (str(len(student.completed_courses)), "Completed", ACCENT),
            (str(len(student.active_schedule)),   "Active",    WARNING),
        ]
        for val, label, color in stats:
            stat_frame = tk.Frame(self.stu_sidebar, bg=BG_CARD)
            stat_frame.pack(fill="x", padx=24, pady=6)
            tk.Label(stat_frame, text=val, bg=BG_CARD, fg=color,
                     font=(FONT_FAMILY, 20, "bold")).pack(anchor="w")
            tk.Label(stat_frame, text=label, bg=BG_CARD, fg=TEXT_DIM,
                     font=(FONT_FAMILY, 8)).pack(anchor="w")

        # Divider
        tk.Frame(self.stu_sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=18)

        # Email
        if student.email:
            tk.Label(self.stu_sidebar, text="Email", bg=BG_CARD, fg=TEXT_DIM, font=(FONT_FAMILY, 8, "bold")).pack(anchor="w", padx=24)
            tk.Label(self.stu_sidebar, text=student.email, bg=BG_CARD, fg=TEXT_SECONDARY, font=(FONT_FAMILY, 9), wraplength=185, justify="left").pack(anchor="w", padx=24, pady=(2, 0))
        # Refresh only the currently visible section; the others will
        # refresh lazily when the user navigates to them via _show_stu_section.
        refresh_map = {
            "transcript": self._refresh_transcript,
            "register":   self._refresh_register_view,
            "schedule":   self._refresh_schedule_view,
        }
        refresh_map[self._stu_active_section]()


    # ─── Transcript ─────────────────────────────────────────────

    def _build_transcript_view(self):
        parent = self.stu_transcript_tab
        hdr = ttk.Frame(parent, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=14)
        ttk.Label(hdr_inner, text="Transcript", font=(FONT_FAMILY, 15, "bold"), foreground=TEXT_PRIMARY, style="Surface.TLabel").pack(side="left")
        ttk.Separator(parent, orient="horizontal").pack(fill="x")
        tree_wrap = ttk.Frame(parent, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("course", "grade", "points")
        self.transcript_tree = ttk.Treeview(tree_wrap, columns=cols, show="headings")
        for col, heading, w, anchor in [("course","Course Name",0,"w"),("grade","Grade",80,"center"),("points","Quality Points",130,"center")]:
            self.transcript_tree.heading(col, text=heading)
            self.transcript_tree.column(col, width=w, anchor=anchor, stretch=(col=="course"))
        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.transcript_tree.yview)
        self.transcript_tree.configure(yscrollcommand=vsb.set)
        self.transcript_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def _refresh_transcript(self):
        for item in self.transcript_tree.get_children(): self.transcript_tree.delete(item)
        username = self.current_user.username
        student = self.uni.students.get(username)
        if not student: return
        for i, (course, grade) in enumerate(student.completed_courses.items()):
            pts = GPA_SCALE.get(grade, 0.0)  # uses the shared constant from registrar
            tag = "even" if i % 2 == 0 else "odd"
            self.transcript_tree.insert("", "end", values=(course, grade, f"{pts:.1f}"), tags=(tag,))
        self.transcript_tree.tag_configure("even", background=TREEVIEW_BG)
        self.transcript_tree.tag_configure("odd", background=TREEVIEW_ALT)

    # ─── Registration ───────────────────────────────────────────

    def _build_register_view(self):
        parent = self.stu_register_tab
        hdr = ttk.Frame(parent, style="Surface.TFrame")
        hdr.pack(fill="x")
        hdr_inner = ttk.Frame(hdr, style="Surface.TFrame")
        hdr_inner.pack(fill="x", padx=24, pady=14)
        ttk.Label(hdr_inner, text="Course Registration", font=(FONT_FAMILY, 15, "bold"), foreground=TEXT_PRIMARY, style="Surface.TLabel").pack(side="left")
        ttk.Button(hdr_inner, text="📝  Enroll in Selected", style="Accent.TButton", command=self._request_enrollment).pack(side="right")
        ttk.Separator(parent, orient="horizontal").pack(fill="x")
        tree_wrap = ttk.Frame(parent, style="TFrame")
        tree_wrap.pack(fill="both", expand=True, padx=20, pady=16)
        cols = ("id", "course", "time", "seats", "waitlist", "status")
        self.reg_tree = ttk.Treeview(tree_wrap, columns=cols, show="headings", selectmode="browse")
        for col, heading, w, anchor in [
            ("id","#",40,"center"),("course","Course",0,"w"),("time","Time Slot",140,"center"),
            ("seats","Seats",70,"center"),("waitlist","Waitlist",70,"center"),("status","Status",130,"center")]:
            self.reg_tree.heading(col, text=heading)
            self.reg_tree.column(col, width=w, anchor=anchor, stretch=(col=="course"))
        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.reg_tree.yview)
        self.reg_tree.configure(yscrollcommand=vsb.set)
        self.reg_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.reg_status_label = ttk.Label(parent, text="", font=FONT_SMALL, foreground=TEXT_SECONDARY)
        self.reg_status_label.pack(anchor="w", padx=20, pady=(0, 8))

    def _refresh_register_view(self):
        for item in self.reg_tree.get_children(): self.reg_tree.delete(item)
        username = self.current_user.username
        student = self.uni.students.get(username)
        if not student: return
        for i, o in enumerate(self.uni.offerings):
            seats = o.seats_available
            wl = len(o.waitlist)
            if username in o.enrolled_students: status = "✅ Enrolled"
            elif username in o.waitlist:
                pos = o.waitlist.position_of(username)
                status = f"⏳ Waitlist #{pos}"
            else: status = "Available" if not o.is_full else "Full"
            tag = "enrolled" if "Enrolled" in status else ("waitlist_row" if "Waitlist" in status else ("even" if i % 2 == 0 else "odd"))
            self.reg_tree.insert("", "end", values=(i + 1, f"{o.course.dept} {o.course.number}: {o.course.name}", o.time_slot, max(seats, 0), wl, status), tags=(tag,))
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
        username = self.current_user.username

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
        username = self.current_user.username
        student = self.uni.students.get(username)
        if not student:
            return
        # Build a display_name → offering dict once (O(n)) so each
        # schedule entry is resolved in O(1) instead of O(n).
        offering_lookup = {o.display_name: o for o in self.uni.offerings}
        for i, offering_name in enumerate(student.active_schedule):
            o = offering_lookup.get(offering_name)
            if o:
                tag = "even" if i % 2 == 0 else "odd"
                self.schedule_tree.insert("", "end", values=(
                    o.course.name, o.section, o.time_slot, f"{o.quarter} {o.year}"
                ), tags=(tag,))
        self.schedule_tree.tag_configure("even", background=TREEVIEW_BG)
        self.schedule_tree.tag_configure("odd", background=TREEVIEW_ALT)


# ═══════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityApp(root)
    root.mainloop()