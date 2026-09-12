import tkinter as tk
from tkinter import ttk


# ------------------------------------------------------------
# COLORS
# ------------------------------------------------------------

PRIMARY = "#E23744"
PRIMARY_DARK = "#C92F3B"

BACKGROUND = "#F5F5F5"
WHITE = "#FFFFFF"

TEXT = "#222222"
SECONDARY_TEXT = "#777777"

GREEN = "#27AE60"
BLUE = "#3498DB"
ORANGE = "#F39C12"
DARK = "#333333"


# ------------------------------------------------------------
# FONTS
# ------------------------------------------------------------

FONT_TITLE = ("Arial", 28, "bold")
FONT_HEADING = ("Arial", 18, "bold")
FONT_SUBHEADING = ("Arial", 14, "bold")
FONT_NORMAL = ("Arial", 10)
FONT_BUTTON = ("Arial", 10, "bold")


# ------------------------------------------------------------
# CONFIGURE TKINTER STYLES
# ------------------------------------------------------------

def configure_styles():

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except:
        pass

    style.configure(
        "Treeview",
        background=WHITE,
        foreground=TEXT,
        rowheight=35,
        fieldbackground=WHITE,
        font=FONT_NORMAL
    )

    style.configure(
        "Treeview.Heading",
        background=PRIMARY,
        foreground=WHITE,
        font=("Arial", 10, "bold"),
        padding=8
    )

    style.map(
        "Treeview",
        background=[
            ("selected", "#FFD9DC")
        ],
        foreground=[
            ("selected", TEXT)
        ]
    )

    style.configure(
        "TCombobox",
        padding=7
    )

    style.configure(
        "TProgressbar",
        thickness=12
    )


# ------------------------------------------------------------
# BUTTON CREATOR
# ------------------------------------------------------------

def create_button(
    parent,
    text,
    command,
    bg=PRIMARY,
    fg=WHITE
):

    return tk.Button(
        parent,
        text=text,
        command=command,
        font=FONT_BUTTON,
        bg=bg,
        fg=fg,
        activebackground=PRIMARY_DARK,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        padx=18,
        pady=9,
        cursor="hand2"
    )


# ------------------------------------------------------------
# CARD CREATOR
# ------------------------------------------------------------

def create_card(
    parent,
    icon,
    title,
    value,
    accent
):

    frame = tk.Frame(
        parent,
        bg=WHITE,
        height=130
    )

    frame.pack_propagate(False)

    tk.Label(
        frame,
        text=icon,
        font=("Arial", 23),
        bg=WHITE
    ).pack(
        anchor="w",
        padx=18,
        pady=(12, 0)
    )

    tk.Label(
        frame,
        text=title,
        font=("Arial", 10),
        bg=WHITE,
        fg=SECONDARY_TEXT
    ).pack(
        anchor="w",
        padx=18
    )

    tk.Label(
        frame,
        text=value,
        font=("Arial", 18, "bold"),
        bg=WHITE,
        fg=accent
    ).pack(
        anchor="w",
        padx=18,
        pady=(3, 10)
    )

    return frame