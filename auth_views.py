"""Authentication views for login and registration."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import re

FONT_FAMILY = "Segoe UI"

class LoginFrame(ttk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, style="TFrame")
        self.app = app_controller
        
        # Center card
        self.card = ttk.Frame(self, style="Surface.TFrame")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)
        
        # Title
        ttk.Label(self.card, text="Welcome Back", font=(FONT_FAMILY, 24, "bold"), 
                  style="Surface.TLabel").pack(pady=(30, 5))
        ttk.Label(self.card, text="Please enter your details to sign in", font=(FONT_FAMILY, 10), 
                  foreground="#94a3b8", style="Surface.TLabel").pack(pady=(0, 20))
        
        # Form Container
        form = ttk.Frame(self.card, style="Surface.TFrame")
        form.pack(fill="both", expand=True, padx=40)
        
        # Username / Email
        ttk.Label(form, text="Username or Email", font=(FONT_FAMILY, 9, "bold"), 
                  foreground="#475569", style="Surface.TLabel").pack(anchor="w", pady=(10, 2))
        self.user_var = tk.StringVar()
        self.user_entry = ttk.Entry(form, textvariable=self.user_var, font=(FONT_FAMILY, 11))
        self.user_entry.pack(fill="x", ipady=4)
        
        # Password
        ttk.Label(form, text="Password", font=(FONT_FAMILY, 9, "bold"), 
                  foreground="#475569", style="Surface.TLabel").pack(anchor="w", pady=(15, 2))
        self.pwd_var = tk.StringVar()
        self.pwd_entry = ttk.Entry(form, textvariable=self.pwd_var, font=(FONT_FAMILY, 11), show="•")
        self.pwd_entry.pack(fill="x", ipady=4)
        
        # Role
        role_frame = ttk.Frame(form, style="Surface.TFrame")
        role_frame.pack(fill="x", pady=(15, 20))
        ttk.Label(role_frame, text="Log in as:", font=(FONT_FAMILY, 9, "bold"), 
                  foreground="#475569", style="Surface.TLabel").pack(side="left", padx=(0, 10))
        self.role_var = tk.StringVar(value="Student")
        ttk.Radiobutton(role_frame, text="Student", variable=self.role_var, value="Student", style="TRadiobutton").pack(side="left", padx=5)
        ttk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="Admin", style="TRadiobutton").pack(side="left", padx=5)
        
        # Submit
        ttk.Button(form, text="Sign In", style="Accent.TButton", 
                   command=self.submit_login).pack(fill="x", pady=(5, 10), ipady=4)
        
        # Register link
        link_frame = ttk.Frame(form, style="Surface.TFrame")
        link_frame.pack(pady=10)
        ttk.Label(link_frame, text="Don't have an account?", font=(FONT_FAMILY, 10), 
                  foreground="#94a3b8", style="Surface.TLabel").pack(side="left")
        
        # simulated link button (using standard button for now or a stylized label bind)
        reg_lbl = ttk.Label(link_frame, text=" Sign up", font=(FONT_FAMILY, 10, "bold"), 
                            foreground="#4f46e5", cursor="hand2", style="Surface.TLabel")
        reg_lbl.pack(side="left")
        reg_lbl.bind("<Button-1>", lambda e: self.app.show_register())


    def submit_login(self):
        user = self.user_var.get().strip()
        pwd = self.pwd_var.get().strip()
        role = self.role_var.get()
        self.app.login_action(user, pwd, role)


class RegisterFrame(ttk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, style="TFrame")
        self.app = app_controller
        self.avatar_filepath = ""
        
        # Center card
        self.card = ttk.Frame(self, style="Surface.TFrame")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=620)
        
        # Title
        ttk.Label(self.card, text="Create Account", font=(FONT_FAMILY, 24, "bold"), 
                  style="Surface.TLabel").pack(pady=(20, 5))
        ttk.Label(self.card, text="Join the University platform", font=(FONT_FAMILY, 10), 
                  foreground="#94a3b8", style="Surface.TLabel").pack(pady=(0, 15))
        
        # Form Container
        form = ttk.Frame(self.card, style="Surface.TFrame")
        form.pack(fill="both", expand=True, padx=40)
        
        # Name Row
        name_row = ttk.Frame(form, style="Surface.TFrame")
        name_row.pack(fill="x", pady=(5, 10))
        
        f1 = ttk.Frame(name_row, style="Surface.TFrame")
        f1.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Label(f1, text="First Name", font=(FONT_FAMILY, 9, "bold"), foreground="#475569", style="Surface.TLabel").pack(anchor="w")
        self.first_var = tk.StringVar()
        ttk.Entry(f1, textvariable=self.first_var, font=(FONT_FAMILY, 10)).pack(fill="x", ipady=3)
        
        f2 = ttk.Frame(name_row, style="Surface.TFrame")
        f2.pack(side="left", fill="x", expand=True, padx=(5, 0))
        ttk.Label(f2, text="Last Name", font=(FONT_FAMILY, 9, "bold"), foreground="#475569", style="Surface.TLabel").pack(anchor="w")
        self.last_var = tk.StringVar()
        ttk.Entry(f2, textvariable=self.last_var, font=(FONT_FAMILY, 10)).pack(fill="x", ipady=3)

        # Credentials Row
        cred_row = ttk.Frame(form, style="Surface.TFrame")
        cred_row.pack(fill="x", pady=(0, 10))
        
        c1 = ttk.Frame(cred_row, style="Surface.TFrame")
        c1.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Label(c1, text="Username", font=(FONT_FAMILY, 9, "bold"), foreground="#475569", style="Surface.TLabel").pack(anchor="w")
        self.user_var = tk.StringVar()
        ttk.Entry(c1, textvariable=self.user_var, font=(FONT_FAMILY, 10)).pack(fill="x", ipady=3)
        
        c2 = ttk.Frame(cred_row, style="Surface.TFrame")
        c2.pack(side="left", fill="x", expand=True, padx=(5, 0))
        ttk.Label(c2, text="DOB (YYYY-MM-DD)", font=(FONT_FAMILY, 9, "bold"), foreground="#475569", style="Surface.TLabel").pack(anchor="w")
        self.dob_var = tk.StringVar()
        ttk.Entry(c2, textvariable=self.dob_var, font=(FONT_FAMILY, 10)).pack(fill="x", ipady=3)

        # Email
        ttk.Label(form, text="Email", font=(FONT_FAMILY, 9, "bold"), foreground="#475569", style="Surface.TLabel").pack(anchor="w", pady=(0, 2))
        self.email_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.email_var, font=(FONT_FAMILY, 10)).pack(fill="x", ipady=3)

        # Password
        ttk.Label(form, text="Password (min 6 chars)", font=(FONT_FAMILY, 9, "bold"), foreground="#475569", style="Surface.TLabel").pack(anchor="w", pady=(10, 2))
        self.pwd_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.pwd_var, font=(FONT_FAMILY, 10), show="•").pack(fill="x", ipady=3)

        # Profile Image
        img_row = ttk.Frame(form, style="Surface.TFrame")
        img_row.pack(fill="x", pady=15)
        ttk.Label(img_row, text="Profile Image", font=(FONT_FAMILY, 9, "bold"), foreground="#475569", style="Surface.TLabel").pack(side="left")
        ttk.Button(img_row, text="Choose File...", command=self.choose_image).pack(side="left", padx=10)
        self.img_label = ttk.Label(img_row, text="No file chosen", font=(FONT_FAMILY, 8), foreground="#94a3b8", style="Surface.TLabel")
        self.img_label.pack(side="left")

        # Role
        role_frame = ttk.Frame(form, style="Surface.TFrame")
        role_frame.pack(fill="x", pady=(5, 15))
        ttk.Label(role_frame, text="Register as:", font=(FONT_FAMILY, 9, "bold"), foreground="#475569", style="Surface.TLabel").pack(side="left", padx=(0, 10))
        self.role_var = tk.StringVar(value="Student")
        ttk.Radiobutton(role_frame, text="Student", variable=self.role_var, value="Student").pack(side="left", padx=5)
        ttk.Radiobutton(role_frame, text="Admin", variable=self.role_var, value="Admin").pack(side="left", padx=5)

        # Submit
        ttk.Button(form, text="Create Account", style="Accent.TButton", 
                   command=self.submit_register).pack(fill="x", pady=(5, 10), ipady=4)
        
        # Back to Login
        link_frame = ttk.Frame(form, style="Surface.TFrame")
        link_frame.pack(pady=5)
        ttk.Label(link_frame, text="Already have an account?", font=(FONT_FAMILY, 10), 
                  foreground="#94a3b8", style="Surface.TLabel").pack(side="left")
        log_lbl = ttk.Label(link_frame, text=" Sign in", font=(FONT_FAMILY, 10, "bold"), 
                            foreground="#4f46e5", cursor="hand2", style="Surface.TLabel")
        log_lbl.pack(side="left")
        log_lbl.bind("<Button-1>", lambda e: self.app.show_login())

    def choose_image(self):
        filepath = filedialog.askopenfilename(
            title="Select Profile Image",
            filetypes=(("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
        )
        if filepath:
            self.avatar_filepath = filepath
            filename = os.path.basename(filepath)
            self.img_label.config(text=filename[:20] + ("..." if len(filename)>20 else ""))

    def submit_register(self):
        first = self.first_var.get().strip()
        last = self.last_var.get().strip()
        user = self.user_var.get().strip()
        dob = self.dob_var.get().strip()
        email = self.email_var.get().strip()
        pwd = self.pwd_var.get().strip()
        role = self.role_var.get()

        if not all([first, last, user, dob, email, pwd]):
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        # Basic email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Validation Error", "Invalid email format.")
            return

        if len(pwd) < 6:
            messagebox.showwarning("Validation Error", "Password must be at least 6 characters.")
            return

        success, msg = self.app.register_action(first, last, user, dob, email, pwd, role, self.avatar_filepath)
        if success:
            messagebox.showinfo("Success", msg)
            self.app.show_login()
        else:
            messagebox.showerror("Error", msg)
