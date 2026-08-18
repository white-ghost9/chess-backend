# employee_form.py
# Handles both "Add Employee" and "Edit Employee" forms.
# The form body is wrapped in a scrollable canvas so all fields
# remain accessible even on smaller screens.

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import PhotoImage
from tkcalendar import DateEntry

from . import database
from . import styles
from . import utils


# ==========================================================
# Photo Preview Helper
def load_photo(path, max_size=120):
    """Load and resize an image from path for preview. Returns None on failure."""
    if not path or not os.path.exists(path):
        return None
    try:
        img = PhotoImage(file=path)
        # Resize to fit within max_size while keeping aspect ratio
        ratio = img.width() / max_size
        new_width = max_size
        new_height = int(img.height() / ratio)
        if new_height > max_size:
            ratio = img.height() / max_size
            new_height = max_size
            new_width = int(img.width() / ratio)
        return img.subsample(
            max(1, img.width() // new_width), max(1, img.height() // new_height)
        )
    except Exception:
        return None


# ==========================================================
# Employee Form (Add / Edit)
# ==========================================================


def open_form(parent_window, refresh_callback, edit_data=None):
    """Open the employee form.

    Args:
        parent_window: parent Tk window.
        refresh_callback: called after a successful save to refresh the dashboard.
        edit_data: tuple of employee data (id, emp_id, name, department, position,
                   email, phone, salary, join_date, photo). If None, the form is in
                   "Add" mode, otherwise in "Edit" mode.
    """
    is_edit = edit_data is not None

    form = tk.Toplevel(parent_window)
    form.title("Edit Employee" if is_edit else "Add New Employee")
    form.geometry("550x760")
    form.configure(bg=styles.BG_COLOR)
    form.resizable(True, True)
    form.state("zoomed")  # Open in maximized position
    form.grab_set()

    tk.Label(
        form,
        text="Edit Employee" if is_edit else "Add Employee",
        bg=styles.BG_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.TITLE_FONT,
    ).pack(pady=20)

    # ======================================================
    # Scrollable Body
    # ======================================================
    body_frame = tk.Frame(form, bg=styles.BG_COLOR)
    body_frame.pack(fill="both", expand=True, padx=30)

    # Canvas + vertical scrollbar for scrolling the form fields
    canvas = tk.Canvas(
        body_frame,
        bg=styles.BG_COLOR,
        highlightthickness=0,
        bd=0,
    )
    scrollbar = ttk.Scrollbar(
        body_frame,
        orient="vertical",
        command=canvas.yview,
    )
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Inner frame that holds all the form fields
    container = tk.Frame(canvas, bg=styles.BG_COLOR)
    canvas_window = canvas.create_window(
        (0, 0),
        window=container,
        anchor="nw",
    )

    # Keep the inner frame width matched to the canvas width
    def _on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", _on_canvas_configure)

    # Update scroll region whenever the inner frame size changes
    def _on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    container.bind("<Configure>", _on_frame_configure)

    # Enable mouse-wheel scrolling when hovering over the form body
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Disable global mousewheel binding when the form is destroyed
    def _on_close():
        canvas.unbind_all("<MouseWheel>")
        form.destroy()

    form.protocol("WM_DELETE_WINDOW", _on_close)

    entries = {}

    def add_entry(label):
        tk.Label(
            container,
            text=label,
            bg=styles.BG_COLOR,
            fg=styles.TEXT_COLOR,
            font=styles.NORMAL_FONT,
            anchor="w",
        ).pack(fill="x", pady=(8, 2))

        entry = tk.Entry(container, font=styles.NORMAL_FONT)
        entry.pack(fill="x", ipady=6)

        entries[label] = entry

    # Text fields
    add_entry("Full Name")
    add_entry("Email")
    add_entry("Phone Number")
    add_entry("Salary")

    # Department
    tk.Label(
        container,
        text="Department",
        bg=styles.BG_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.NORMAL_FONT,
    ).pack(fill="x", pady=(8, 2))

    department = ttk.Combobox(
        container,
        values=[
            "IT",
            "HR",
            "Finance",
            "Sales",
            "Marketing",
            "Operations",
        ],
        state="readonly",
        font=styles.NORMAL_FONT,
    )
    department.pack(fill="x")
    department.current(0)

    # Position
    tk.Label(
        container,
        text="Position",
        bg=styles.BG_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.NORMAL_FONT,
    ).pack(fill="x", pady=(8, 2))

    position = ttk.Combobox(
        container,
        values=[
            "Manager",
            "Senior Executive",
            "Executive",
            "Developer",
            "Designer",
            "Intern",
        ],
        state="readonly",
        font=styles.NORMAL_FONT,
    )
    position.pack(fill="x")
    position.current(0)

    # Calendar
    tk.Label(
        container,
        text="Join Date",
        bg=styles.BG_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.NORMAL_FONT,
    ).pack(fill="x", pady=(8, 2))

    join_date = DateEntry(
        container,
        date_pattern="yyyy-mm-dd",
        font=styles.NORMAL_FONT,
    )
    join_date.pack(fill="x")

    # Photo
    tk.Label(
        container,
        text="Photo",
        bg=styles.BG_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.NORMAL_FONT,
    ).pack(fill="x", pady=(8, 2))

    photo_var = tk.StringVar()
    photo_preview = tk.Label(container, bg=styles.CARD_COLOR, text="No photo")

    photo_frame = tk.Frame(container, bg=styles.BG_COLOR)
    photo_frame.pack(fill="x")

    photo_entry = tk.Entry(
        photo_frame,
        textvariable=photo_var,
        font=styles.NORMAL_FONT,
    )
    photo_entry.pack(side="left", fill="x", expand=True)

    def update_preview():
        path = photo_var.get().strip()
        img = load_photo(path)
        if img:
            photo_preview.config(image=img, text="")
            form.after(100, lambda: setattr(photo_preview, "_img", img))
        else:
            photo_preview.config(image="", text="No photo")
        photo_preview.pack(pady=(8, 0))

    def browse_photo():
        file = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif"),
                ("All Files", "*.*"),
            ],
        )
        if file:
            photo_var.set(file)
            update_preview()

    tk.Button(
        photo_frame,
        text="📁 Browse",
        bg=styles.BUTTON_COLOR,
        activebackground=styles.BUTTON_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=browse_photo,
    ).pack(side="right", padx=(8, 0), ipady=3)

    # Inline Save/Update button next to Browse so it's always visible
    inline_save_text = "💾 Save / Update" if is_edit else "💾 Save"
    tk.Button(
        photo_frame,
        text=inline_save_text,
        bg=styles.SUCCESS_COLOR,
        activebackground=styles.SUCCESS_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=save_employee,
    ).pack(side="right", padx=(8, 0), ipady=3)

    photo_preview.pack(pady=(8, 0))

    # ======================================================
    # Pre-fill data in Edit mode
    # ======================================================
    if is_edit:
        # edit_data indices: 0=id, 1=emp_id, 2=name, 3=dept, 4=pos,
        #                    5=email, 6=phone, 7=salary, 8=join_date, 9=photo
        entries["Full Name"].insert(0, edit_data[2])
        department.set(edit_data[3])
        position.set(edit_data[4])
        entries["Email"].insert(0, edit_data[5])
        entries["Phone Number"].insert(0, edit_data[6])
        entries["Salary"].insert(0, str(edit_data[7]))
        join_date.set_date(edit_data[8])
        if edit_data[9]:
            photo_var.set(edit_data[9])
            update_preview()

    # ======================================================
    # Save Employee (Add or Update)
    # ======================================================
    def save_employee():
        name = entries["Full Name"].get().strip()
        email = entries["Email"].get().strip()
        phone = entries["Phone Number"].get().strip()
        salary_text = entries["Salary"].get().strip()

        dept = department.get()
        pos = position.get()
        date = join_date.get_date().strftime("%Y-%m-%d")
        photo = photo_var.get().strip()

        if not all([name, email, phone, salary_text]):
            messagebox.showerror(
                "Validation Error",
                "Please fill all required fields.",
                parent=form,
            )
            return

        if not utils.validate_email(email):
            messagebox.showerror(
                "Validation Error",
                "Please enter a valid email address.",
                parent=form,
            )
            return

        if not utils.validate_phone(phone):
            messagebox.showerror(
                "Validation Error",
                "Phone number must contain only digits (7-15 digits).",
                parent=form,
            )
            return

        try:
            salary = float(salary_text)
            if salary <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Salary must be a positive number.",
                parent=form,
            )
            return

        if is_edit:
            emp_id = edit_data[1]
            success, message = database.update_employee(
                emp_id=emp_id,
                name=name,
                department=dept,
                position=pos,
                email=email,
                phone=phone,
                salary=salary,
                join_date=date,
                photo=photo,
            )
        else:
            success, message = database.add_employee(
                name=name,
                department=dept,
                position=pos,
                email=email,
                phone=phone,
                salary=salary,
                join_date=date,
                photo=photo,
            )

        if success:
            messagebox.showinfo("Success", message, parent=form)
            refresh_callback()
            _on_close()
        else:
            messagebox.showerror("Duplicate Employee", message, parent=form)

    # ======================================================
    # Buttons (fixed at the bottom)
    # ======================================================
    button_frame = tk.Frame(form, bg=styles.BG_COLOR)
    button_frame.pack(fill="x", pady=20)

    save_button_text = "💾 Save / Update" if is_edit else "💾 Save Employee"

    tk.Button(
        button_frame,
        text=save_button_text,
        bg=styles.SUCCESS_COLOR,
        activebackground=styles.SUCCESS_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=18,
        relief="flat",
        cursor="hand2",
        command=save_employee,
    ).pack(side="left", padx=20, ipady=4)

    tk.Button(
        button_frame,
        text="✖ Cancel",
        bg=styles.DANGER_COLOR,
        activebackground=styles.DANGER_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=12,
        relief="flat",
        cursor="hand2",
        command=_on_close,
    ).pack(side="right", padx=20, ipady=4)
