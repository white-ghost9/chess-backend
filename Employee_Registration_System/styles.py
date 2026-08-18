"""
Modern, polished styling module for the Tkinter Employee Registration System.

This design language is translated from the provided Qt/CustomTkinter theme:
- Light background (#F7FAFC)
- White cards (#FFFFFF)
- Blue accent (#3182CE)
- Modern, soft UI with rounded corners & subtle borders
"""

import tkinter.ttk as ttk

# ==========================================================
# Color Palette (Light Modern Theme)
# ==========================================================

# Main background
BG_COLOR = "#F7FAFC"

# Card / panel background (white)
CARD_COLOR = "#FFFFFF"

# Secondary card / subtle background
CARD_COLOR_LIGHT = "#EDF2F7"

# Header / sidebar background (dark slate)
HEADER_COLOR = "#1A202C"

# Text colors
TEXT_COLOR = "#2D3748"
SUBTEXT_COLOR = "#718096"

# Accent / Primary buttons
BUTTON_COLOR = "#3182CE"
BUTTON_HOVER = "#2B6CB0"
BUTTON_PRESSED = "#2C5282"

# Success
SUCCESS_COLOR = "#38A169"
SUCCESS_HOVER = "#2F855A"

# Danger
DANGER_COLOR = "#E53E3E"
DANGER_HOVER = "#C53030"

# Warning
WARNING_COLOR = "#D69E2E"
WARNING_HOVER = "#B7791F"

# Info
INFO_COLOR = "#3182CE"
INFO_HOVER = "#2B6CB0"

# Purple
PURPLE_COLOR = "#805AD5"
PURPLE_HOVER = "#6B46C1"

# Gray / Secondary
GRAY_COLOR = "#A0AEC0"
GRAY_HOVER = "#718096"

# Borders & outlines
OUTLINE_COLOR = "#CBD5E0"
ACCENT_COLOR = "#3182CE"

# Table selection
SELECTION_BG = "#EBF8FF"
SELECTION_FG = "#2B6CB0"

# ==========================================================
# Fonts
# ==========================================================

TITLE_FONT = ("Segoe UI", 20, "bold")
SUBTITLE_FONT = ("Segoe UI", 14, "bold")
NORMAL_FONT = ("Segoe UI", 11)
SMALL_FONT = ("Segoe UI", 9)
HEADER_FONT = ("Segoe UI", 16, "bold")

# ==========================================================
# ttk Styling
# ==========================================================


def apply_styles():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Base
    style.configure(
        ".",
        background=BG_COLOR,
        foreground=TEXT_COLOR,
        fieldbackground="#FFFFFF",
        font=NORMAL_FONT,
    )

    # ============ Treeview (Data Table) ============
    style.configure(
        "Treeview",
        background="#FFFFFF",
        foreground=TEXT_COLOR,
        rowheight=34,
        fieldbackground="#FFFFFF",
        font=NORMAL_FONT,
        borderwidth=1,
        relief="solid",
    )

    style.configure(
        "Treeview.Heading",
        background="#F7FAFC",
        foreground="#4A5568",
        font=("Segoe UI", 10, "bold"),
        padding=(8, 8),
        borderwidth=0,
        relief="flat",
    )

    style.map(
        "Treeview",
        background=[
            ("selected", SELECTION_BG),
            ("!selected", "#FFFFFF"),
        ],
        foreground=[
            ("selected", SELECTION_FG),
            ("!selected", TEXT_COLOR),
        ],
    )

    style.map(
        "Treeview.Heading",
        background=[("active", "#EDF2F7")],
        foreground=[("active", "#2D3748")],
    )

    # ============ Buttons ============
    style.configure(
        "TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(14, 8),
        borderwidth=0,
        relief="flat",
    )

    style.map(
        "TButton",
        background=[
            ("active", BUTTON_HOVER),
            ("pressed", BUTTON_PRESSED),
        ],
        foreground=[("disabled", "#A0AEC0")],
    )

    # Primary button
    style.configure("Primary.TButton", background=BUTTON_COLOR, foreground="#FFFFFF")
    style.map(
        "Primary.TButton",
        background=[("active", BUTTON_HOVER), ("pressed", BUTTON_PRESSED)],
    )

    # Success button
    style.configure("Success.TButton", background=SUCCESS_COLOR, foreground="#FFFFFF")
    style.map(
        "Success.TButton",
        background=[("active", SUCCESS_HOVER), ("pressed", "#276749")],
    )

    # Danger button
    style.configure("Danger.TButton", background=DANGER_COLOR, foreground="#FFFFFF")
    style.map(
        "Danger.TButton",
        background=[("active", DANGER_HOVER), ("pressed", "#9B2C2C")],
    )

    # Warning button
    style.configure("Warning.TButton", background=WARNING_COLOR, foreground="#FFFFFF")
    style.map(
        "Warning.TButton",
        background=[("active", WARNING_HOVER), ("pressed", "#975A16")],
    )

    # Info button
    style.configure("Info.TButton", background=INFO_COLOR, foreground="#FFFFFF")
    style.map(
        "Info.TButton",
        background=[("active", INFO_HOVER), ("pressed", "#2C5282")],
    )

    # Purple button
    style.configure("Purple.TButton", background=PURPLE_COLOR, foreground="#FFFFFF")
    style.map(
        "Purple.TButton",
        background=[("active", PURPLE_HOVER), ("pressed", "#553C9A")],
    )

    # Gray / secondary button
    style.configure("Gray.TButton", background=GRAY_COLOR, foreground="#FFFFFF")
    style.map(
        "Gray.TButton",
        background=[("active", GRAY_HOVER), ("pressed", "#4A5568")],
    )

    # ============ Combobox ============
    style.configure(
        "TCombobox",
        font=NORMAL_FONT,
        padding=6,
        fieldbackground="#FFFFFF",
        background="#FFFFFF",
        foreground=TEXT_COLOR,
        arrowcolor="#718096",
        bordercolor=OUTLINE_COLOR,
        lightcolor=OUTLINE_COLOR,
        darkcolor=OUTLINE_COLOR,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", "#FFFFFF")],
        foreground=[("readonly", TEXT_COLOR)],
        bordercolor=[("focus", ACCENT_COLOR)],
    )

    # ============ Entry ============
    style.configure(
        "TEntry",
        padding=6,
        fieldbackground="#FFFFFF",
        foreground=TEXT_COLOR,
        bordercolor=OUTLINE_COLOR,
        lightcolor=OUTLINE_COLOR,
        darkcolor=OUTLINE_COLOR,
    )
    style.map(
        "TEntry",
        bordercolor=[("focus", ACCENT_COLOR)],
    )

    # ============ Scrollbar ============
    style.configure(
        "Vertical.TScrollbar",
        background="#CBD5E0",
        troughcolor="#F7FAFC",
        bordercolor="#F7FAFC",
        arrowcolor="#718096",
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", "#A0AEC0")],
    )

    # ============ DateEntry ============
    style.configure(
        "DateEntry",
        fieldbackground="#FFFFFF",
        background="#FFFFFF",
        foreground=TEXT_COLOR,
        arrowcolor="#718096",
        padding=6,
    )


# ==========================================================
# Reference: Original Qt QSS + CustomTkinter theme tokens
# (Kept for documentation / future PyQt or CustomTkinter port)
# ==========================================================

APP_STYLESHEET = """
/* Light modern theme for Qt widgets */
QMainWindow, QDialog {
    background-color: #F7FAFC;
}
QPushButton {
    background-color: #3182CE;
    color: #FFFFFF;
    font-weight: 600;
    padding: 9px 18px;
    border-radius: 6px;
    border: none;
}
QPushButton:hover {
    background-color: #2B6CB0;
}
QPushButton#btn_danger {
    background-color: #E53E3E;
}
QPushButton#btn_danger:hover {
    background-color: #C53030;
}
QPushButton#btn_success {
    background-color: #38A169;
}
QPushButton#btn_success:hover {
    background-color: #2F855A;
}
QLineEdit, QComboBox, QDateEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E0;
    border-radius: 6px;
    padding: 8px 12px;
    color: #2D3748;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 2px solid #3182CE;
}
QTableWidget, QTableView {
    background-color: #FFFFFF;
    gridline-color: #EDF2F7;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    selection-background-color: #EBF8FF;
    selection-color: #2B6CB0;
}
QHeaderView::section {
    background-color: #F7FAFC;
    color: #4A5568;
    font-weight: 700;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #E2E8F0;
}
"""

# CustomTkinter color dictionary (alternative UI)
CTK_THEME = {
    "bg_light": "#F7FAFC",
    "bg_dark": "#1A202C",
    "bg_card": "#FFFFFF",
    "text_primary": "#2D3748",
    "text_secondary": "#718096",
    "accent_primary": "#3182CE",
    "accent_hover": "#2B6CB0",
    "danger": "#E53E3E",
    "danger_hover": "#C53030",
    "success": "#38A169",
    "success_hover": "#2F855A",
    "border": "#E2E8F0",
}
