"""Shared theme constants and ttk style configuration."""

from tkinter import ttk

# COLOR PALETTE
BG_DARK        = "#f0f2f5"   # main window background — soft gray
BG_SURFACE     = "#ffffff"   # surface panels — white
BG_CARD        = "#f8f9fc"   # card backgrounds — very light blue-gray
BG_INPUT       = "#ffffff"   # text-entry fields

ACCENT         = "#4f46e5"   # primary indigo
ACCENT_HOVER   = "#6366f1"   # hover state
ACCENT_DIM     = "#818cf8"   # softer accent (nav glows, footer label)

SUCCESS        = "#16a34a"   # green
WARNING        = "#d97706"   # amber
DANGER         = "#dc2626"   # red

TEXT_PRIMARY   = "#1e293b"   # near-black
TEXT_SECONDARY = "#475569"   # slate-gray
TEXT_DIM       = "#94a3b8"   # light slate

BORDER         = "#e2e8f0"   # soft border / divider

TREEVIEW_BG    = "#ffffff"   # tree row background
TREEVIEW_FG    = "#1e293b"   # tree row foreground
TREEVIEW_SEL   = "#4f46e5"   # selected row background
TREEVIEW_ALT   = "#f1f5f9"   # alternating row background

# TYPOGRAPHY
FONT_FAMILY  = "Segoe UI"
FONT_HEADING = (FONT_FAMILY, 20, "bold")
FONT_SUBTITLE= (FONT_FAMILY, 13)
FONT_BODY    = (FONT_FAMILY, 10)
FONT_SMALL   = (FONT_FAMILY, 9)
FONT_BUTTON  = (FONT_FAMILY, 10, "bold")
FONT_TAB     = (FONT_FAMILY, 11, "bold")


def configure_styles():
    """Apply the full modern light theme to all ttk widgets. Call once on startup."""
    style = ttk.Style()
    style.theme_use("clam")

    # GLOBAL DEFAULTS
    style.configure(".", background=BG_DARK, foreground=TEXT_PRIMARY, font=FONT_BODY,
                    borderwidth=0, focuscolor=ACCENT)

    # NOTEBOOK
    style.configure("TNotebook", background=BG_DARK, borderwidth=0, padding=0)
    style.configure("TNotebook.Tab", background=BG_SURFACE, foreground=TEXT_SECONDARY,
                    padding=[24, 10], font=FONT_TAB)
    style.map("TNotebook.Tab",
              background=[("selected", ACCENT), ("active", ACCENT_DIM)],
              foreground=[("selected", "#ffffff"), ("active", TEXT_PRIMARY)],
              relief=[("selected", "flat")])

    style.configure("Inner.TNotebook", background=BG_SURFACE, borderwidth=0)
    style.configure("Inner.TNotebook.Tab", background=BG_CARD, foreground=TEXT_SECONDARY,
                    padding=[18, 8], font=FONT_BODY)
    style.map("Inner.TNotebook.Tab",
              background=[("selected", ACCENT_DIM), ("active", BG_CARD)],
              foreground=[("selected", "#ffffff"), ("active", TEXT_PRIMARY)],
              relief=[("selected", "flat")])

    # LABELS
    style.configure("TLabel",        background=BG_DARK,    foreground=TEXT_PRIMARY)
    style.configure("Card.TLabel",   background=BG_CARD)
    style.configure("Surface.TLabel",background=BG_SURFACE)
    style.configure("Heading.TLabel",font=FONT_HEADING, foreground=TEXT_PRIMARY,  background=BG_DARK)
    style.configure("Subtitle.TLabel",font=FONT_SUBTITLE, foreground=TEXT_SECONDARY, background=BG_DARK)
    style.configure("Accent.TLabel", foreground=ACCENT, background=BG_CARD, font=(FONT_FAMILY, 22, "bold"))
    style.configure("Value.TLabel",  foreground=TEXT_PRIMARY, background=BG_CARD, font=(FONT_FAMILY, 11))
    style.configure("Dim.TLabel",    foreground=TEXT_DIM, background=BG_CARD, font=FONT_SMALL)

    # FRAMES
    style.configure("TFrame",         background=BG_DARK)
    style.configure("Card.TFrame",    background=BG_CARD)
    style.configure("Surface.TFrame", background=BG_SURFACE)

    # LABELFRAMES
    style.configure("TLabelframe",       background=BG_SURFACE, foreground=ACCENT,
                    font=(FONT_FAMILY, 11, "bold"), borderwidth=1, relief="groove")
    style.configure("TLabelframe.Label", background=BG_SURFACE, foreground=ACCENT)

    # BUTTONS
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

    # ENTRY
    style.configure("TEntry", fieldbackground=BG_INPUT, foreground=TEXT_PRIMARY,
                    insertcolor=TEXT_PRIMARY, borderwidth=1, padding=[8, 6],
                    relief="solid", bordercolor=BORDER)
    style.map("TEntry",
              fieldbackground=[("focus", "#ffffff")],
              bordercolor=[("focus", ACCENT)])

    # COMBOBOX
    style.configure("TCombobox", fieldbackground=BG_INPUT, foreground=TEXT_PRIMARY,
                    selectbackground=ACCENT, selectforeground="#ffffff",
                    padding=[8, 6], arrowcolor=ACCENT)
    style.map("TCombobox", fieldbackground=[("focus", BG_CARD)])

    # TREEVIEW
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

    # SCROLLBAR
    style.configure("Vertical.TScrollbar", background=BG_SURFACE,
                    troughcolor=BG_DARK, arrowcolor=ACCENT, borderwidth=0)

    # SEPARATOR
    style.configure("TSeparator", background=BORDER)

    return style
