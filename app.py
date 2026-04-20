"""app.py — application entry point and root controller."""

import tkinter as tk
from tkinter import ttk, messagebox

from registrar.institution import Institution
from registrar.models import Student, Admin, hash_password
from utils.image_processing import process_avatar, save_avatar_file
from views.theme import (
    configure_styles,
    FONT_FAMILY, FONT_SMALL,
    BG_DARK, BG_SURFACE,
    ACCENT, ACCENT_DIM, DANGER,
    TEXT_PRIMARY, TEXT_DIM,
    SUCCESS, WARNING,
)
from views.admin_dashboard import AdminDashboard
from views.student_dashboard import StudentDashboard
from views.auth_views import LoginFrame, RegisterFrame


class UniversityApp:
    """Root controller — owns the window, routing, and shared UI chrome."""

    def __init__(self, root):
        self.root = root
        self.root.title("🎓 University Registration System")
        # self.root.geometry("1100x720")
        # self.root.minsize(900, 640)
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)

        # Style combobox listbox colours globally
        self.root.option_add("*TCombobox*Listbox.background",       "#ffffff")
        self.root.option_add("*TCombobox*Listbox.foreground",       "#1e293b")
        self.root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")

        self.style = configure_styles()

        # Load institution data
        self.uni = Institution.load()

        self.current_user = None
        self.current_role = None

        # References set by each dashboard on construction
        self.admin_dashboard   = None
        self.student_dashboard = None

        self.main_container = ttk.Frame(self.root, style="TFrame")
        self.main_container.pack(fill="both", expand=True)

        self.show_login()

    # ROUTING

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_container()
        LoginFrame(self.main_container, self).pack(fill="both", expand=True)

    def show_register(self):
        self.clear_container()
        RegisterFrame(self.main_container, self).pack(fill="both", expand=True)

    def logout(self):
        self.current_user = None
        self.current_role = None
        self.admin_dashboard   = None
        self.student_dashboard = None
        self.show_login()

    def show_dashboard(self):
        self.clear_container()
        self._build_header()

        content_frame = ttk.Frame(self.main_container, style="TFrame")
        content_frame.pack(expand=True, fill="both")

        if self.current_role == "Admin":
            AdminDashboard(content_frame, self).pack(fill="both", expand=True)
        else:
            StudentDashboard(content_frame, self).pack(fill="both", expand=True)

        self._build_status_bar()

    # AUTH ACTIONS

    def login_action(self, username, pwd, role):
        if not username or not pwd:
            messagebox.showwarning("Login Failed", "Username and password required.")
            return

        user_dict = self.uni.students if role == "Student" else self.uni.admins
        user = user_dict.get(username)

        # Also accept login by email address
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
        user_dict = self.uni.students if role == "Student" else self.uni.admins

        if username in user_dict:
            return False, f"Username '{username}' already exists."
        for u in user_dict.values():
            if u.email == email:
                return False, f"Email '{email}' already exists."

        saved_avatar = save_avatar_file(avatar_path, username) if avatar_path else ""

        if role == "Student":
            new_user = Student(first, last, username, dob,
                               email, hash_password(pwd), saved_avatar)
            self.uni.students[username] = new_user
        else:
            new_user = Admin(first, last, username,
                             email, hash_password(pwd), saved_avatar)
            self.uni.admins[username] = new_user

        self.uni._save()
        return True, "Registration successful. Please log in."

    # SHARED UI CHROME

    def _build_header(self):
        header = ttk.Frame(self.main_container, style="Surface.TFrame")
        header.pack(fill="x")
        inner = ttk.Frame(header, style="Surface.TFrame")
        inner.pack(fill="x", padx=30, pady=(16, 12))

        if self.current_role == "Admin":
            # Admin: show avatar + name (no profile sidebar exists for admins)
            self._header_avatar_img = process_avatar(
                getattr(self.current_user, "avatar_path", ""), size=(50, 50))
            if self._header_avatar_img:
                ttk.Label(inner, image=self._header_avatar_img,
                          style="Surface.TLabel").pack(side="left", padx=(0, 15))
            else:
                ttk.Label(inner, text="👤", font=(FONT_FAMILY, 28),
                          style="Surface.TLabel").pack(side="left", padx=(0, 15))

            text_block = ttk.Frame(inner, style="Surface.TFrame")
            text_block.pack(side="left")
            ttk.Label(text_block,
                      text=f"Welcome, {self.current_user.full_name} ({self.current_role})",
                      font=(FONT_FAMILY, 15, "bold"), foreground=TEXT_PRIMARY,
                      style="Surface.TLabel").pack(anchor="w")
            ttk.Label(text_block,
                      text=f"{self.uni.name}  ·  Academic Management System",
                      font=FONT_SMALL, foreground=TEXT_DIM,
                      style="Surface.TLabel").pack(anchor="w")
        else:
            # Student: slim branding bar — the profile sidebar owns avatar/name/stats
            ttk.Label(inner, text="🎓", font=(FONT_FAMILY, 22),
                      style="Surface.TLabel").pack(side="left", padx=(0, 10))
            text_block = ttk.Frame(inner, style="Surface.TFrame")
            text_block.pack(side="left")
            ttk.Label(text_block, text=self.uni.name,
                      font=(FONT_FAMILY, 14, "bold"), foreground=TEXT_PRIMARY,
                      style="Surface.TLabel").pack(anchor="w")
            ttk.Label(text_block, text="Student Portal  ·  Academic Management System",
                      font=FONT_SMALL, foreground=TEXT_DIM,
                      style="Surface.TLabel").pack(anchor="w")

        # Right-side stats (admin only) + sign-out button
        stats = ttk.Frame(inner, style="Surface.TFrame")
        stats.pack(side="right")

        if self.current_role == "Admin":
            self._header_stat_labels = {}
            for key, label, val, color in [
                ("courses",   "Courses",   len(self.uni.catalog),   ACCENT),
                ("students",  "Students",  len(self.uni.students),  SUCCESS),
                ("offerings", "Offerings", len(self.uni.offerings), WARNING),
            ]:
                chip = ttk.Frame(stats, style="Surface.TFrame")
                chip.pack(side="left", padx=12)
                lbl_val = ttk.Label(chip, text=str(val),
                                    font=(FONT_FAMILY, 16, "bold"),
                                    foreground=color, style="Surface.TLabel")
                lbl_val.pack()
                self._header_stat_labels[key] = lbl_val
                ttk.Label(chip, text=label, font=FONT_SMALL,
                          foreground=TEXT_DIM, style="Surface.TLabel").pack()

        logout_chip = ttk.Frame(stats, style="Surface.TFrame")
        logout_chip.pack(side="left", padx=(30, 0))
        ttk.Button(logout_chip, text="🚪 Sign Out", style="Danger.TButton",
                   command=self.logout).pack(pady=4)

    def _refresh_header_stats(self):
        """Update the live stat counters in the admin header (called by admin views)."""
        if not hasattr(self, "_header_stat_labels"):
            return
        labels = self._header_stat_labels
        if "courses"   in labels: labels["courses"].config(text=str(len(self.uni.catalog)))
        if "students"  in labels: labels["students"].config(text=str(len(self.uni.students)))
        if "offerings" in labels: labels["offerings"].config(text=str(len(self.uni.offerings)))

    def _build_status_bar(self):
        bar = ttk.Frame(self.main_container, style="Surface.TFrame")
        bar.pack(fill="x", side="bottom")
        self.status_label = ttk.Label(
            bar,
            text="  System ready",
            font=FONT_SMALL, foreground=TEXT_DIM, style="Surface.TLabel")
        self.status_label.pack(side="left", padx=15, pady=4)
        ttk.Label(bar, text="University Registration System  ",
                  font=FONT_SMALL, foreground=ACCENT_DIM,
                  style="Surface.TLabel").pack(side="right", padx=15, pady=4)

    def _set_status(self, msg):
        """Update the status bar message (called by views after actions)."""
        self.status_label.config(text=f"  {msg}")


# ENTRY POINT

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityApp(root)
    root.mainloop()