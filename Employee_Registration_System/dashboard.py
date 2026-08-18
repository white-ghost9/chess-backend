import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from . import styles
from . import database
from . import employee_form
from . import export
from . import charts


def open_dashboard():
    dash = tk.Tk()
    dash.title("Employee Management Dashboard")
    dash.geometry("1200x700")
    dash.configure(bg=styles.BG_COLOR)
    dash.state("zoomed")  # Open in maximized position
    styles.apply_styles()

    # ======================================================
    # Header
    # ======================================================
    header = tk.Frame(dash, bg=styles.HEADER_COLOR, height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Employee Management Dashboard",
        bg=styles.HEADER_COLOR,
        fg="white",
        font=styles.TITLE_FONT,
    ).pack(side="left", padx=20, pady=15)

    # ======================================================
    # Statistics Cards
    # ======================================================
    stats_frame = tk.Frame(dash, bg=styles.BG_COLOR)
    stats_frame.pack(fill="x", padx=20, pady=15)

    total_card = tk.Frame(stats_frame, bg="#2563eb", width=220, height=100)
    dept_card = tk.Frame(stats_frame, bg="#16a34a", width=220, height=100)
    today_card = tk.Frame(stats_frame, bg="#ea580c", width=220, height=100)

    for card in (total_card, dept_card, today_card):
        card.pack(side="left", padx=10)
        card.pack_propagate(False)

    total_label = tk.Label(
        total_card, text="0", bg="#2563eb", fg="white", font=styles.TITLE_FONT
    )
    total_label.pack(pady=(15, 5))
    tk.Label(
        total_card,
        text="Total Employees",
        bg="#2563eb",
        fg="white",
        font=styles.NORMAL_FONT,
    ).pack()

    dept_label = tk.Label(
        dept_card, text="0", bg="#16a34a", fg="white", font=styles.TITLE_FONT
    )
    dept_label.pack(pady=(15, 5))
    tk.Label(
        dept_card, text="Departments", bg="#16a34a", fg="white", font=styles.NORMAL_FONT
    ).pack()

    today_label = tk.Label(
        today_card, text="0", bg="#ea580c", fg="white", font=styles.TITLE_FONT
    )
    today_label.pack(pady=(15, 5))
    tk.Label(
        today_card,
        text="Joined Today",
        bg="#ea580c",
        fg="white",
        font=styles.NORMAL_FONT,
    ).pack()

    # ======================================================
    # Search Bar
    # ======================================================
    search_frame = tk.Frame(dash, bg=styles.BG_COLOR)
    search_frame.pack(fill="x", padx=20, pady=(5, 10))

    tk.Label(
        search_frame,
        text="Search:",
        bg=styles.BG_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.NORMAL_FONT,
    ).pack(side="left")

    search_var = tk.StringVar()

    search_entry = tk.Entry(
        search_frame, textvariable=search_var, font=styles.NORMAL_FONT, width=40
    )
    search_entry.pack(side="left", padx=10)

    # ======================================================
    # Table + Photo Panel
    # ======================================================
    content_frame = tk.Frame(dash, bg=styles.BG_COLOR)
    content_frame.pack(fill="both", expand=True, padx=20)

    table_frame = tk.Frame(content_frame, bg=styles.BG_COLOR)
    table_frame.pack(side="left", fill="both", expand=True)

    columns = (
        "Employee ID",
        "Name",
        "Department",
        "Position",
        "Email",
        "Phone",
        "Salary",
        "Join Date",
    )

    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Photo display panel
    photo_panel = tk.Frame(
        content_frame, bg=styles.CARD_COLOR, width=240, padx=10, pady=10
    )
    photo_panel.pack(side="right", fill="y", padx=(15, 0))
    photo_panel.pack_propagate(False)

    tk.Label(
        photo_panel,
        text="Employee Photo",
        bg=styles.CARD_COLOR,
        fg=styles.TEXT_COLOR,
        font=styles.SUBTITLE_FONT,
    ).pack(pady=(0, 10))

    photo_label = tk.Label(
        photo_panel,
        text="Select an employee\nto view photo",
        bg=styles.CARD_COLOR,
        fg=styles.SUBTEXT_COLOR,
        font=styles.SMALL_FONT,
    )
    photo_label.pack(fill="both", expand=True)

    # ======================================================
    # Data Functions
    # ======================================================
    def refresh_dashboard():
        for row in tree.get_children():
            tree.delete(row)

        employees = database.get_all_employees()

        for emp in employees:
            tree.insert(
                "",
                "end",
                values=(
                    emp[1],  # emp_id
                    emp[2],  # name
                    emp[3],  # department
                    emp[4],  # position
                    emp[5],  # email
                    emp[6],  # phone
                    emp[7],  # salary
                    emp[8],  # join_date
                ),
            )

        stats = database.get_statistics()
        total_label.config(text=str(stats["total"]))
        dept_label.config(text=str(stats["departments"]))
        today_label.config(text=str(stats["today"]))

    def search_employee():
        keyword = search_var.get().strip()

        for row in tree.get_children():
            tree.delete(row)

        results = (
            database.search_employee(keyword)
            if keyword
            else database.get_all_employees()
        )

        for emp in results:
            tree.insert(
                "",
                "end",
                values=(
                    emp[1],
                    emp[2],
                    emp[3],
                    emp[4],
                    emp[5],
                    emp[6],
                    emp[7],
                    emp[8],
                ),
            )

    def delete_employee():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee.")
            return

        emp_id = tree.item(selected[0])["values"][0]

        confirm = messagebox.askyesno(
            "Delete Employee",
            f"Delete employee {emp_id}?",
        )

        if confirm:
            database.delete_employee(emp_id)
            refresh_dashboard()
            messagebox.showinfo("Deleted", "Employee deleted successfully.")

    def edit_employee():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee.")
            return

        emp_id = tree.item(selected[0])["values"][0]

        # Find the full record (including photo path) in the database
        employee = None
        for emp in database.get_all_employees():
            if emp[1] == emp_id:
                employee = emp
                break

        if employee is None:
            messagebox.showerror("Error", "Employee record not found.")
            return

        employee_form.open_form(dash, refresh_dashboard, edit_data=employee)

    def update_photo_preview(event=None):
        selected = tree.selection()
        if not selected:
            photo_label.config(text="Select an employee\nto view photo", image="")
            return

        emp_id = tree.item(selected[0])["values"][0]

        employee = None
        for emp in database.get_all_employees():
            if emp[1] == emp_id:
                employee = emp
                break

        if employee is None or not employee[9]:
            photo_label.config(text="No photo available", image="")
            return

        path = os.path.abspath(employee[9])
        if not os.path.exists(path):
            photo_label.config(text="Photo file not found", image="")
            return

        try:
            img = Image.open(path)
            img.thumbnail((180, 180), Image.LANCZOS)
            preview = ImageTk.PhotoImage(img)
            photo_label.config(image=preview, text="")
            # Keep a reference so the image is not garbage collected
            photo_label.image = preview
        except Exception:
            photo_label.config(text="Unable to load photo", image="")

    tree.bind("<<TreeviewSelect>>", update_photo_preview)

    # Search Button
    tk.Button(
        search_frame,
        text="🔍 Search",
        bg=styles.BUTTON_COLOR,
        activebackground=styles.BUTTON_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=search_employee,
    ).pack(side="left", padx=5, ipady=3)

    tk.Button(
        search_frame,
        text="🔄 Refresh",
        bg=styles.GRAY_COLOR,
        activebackground=styles.GRAY_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=refresh_dashboard,
    ).pack(side="left", padx=5, ipady=3)

    # ======================================================
    # Bottom Buttons
    # ======================================================
    button_frame = tk.Frame(dash, bg=styles.BG_COLOR)
    button_frame.pack(fill="x", padx=20, pady=15)

    tk.Button(
        button_frame,
        text="＋ Add Employee",
        bg=styles.SUCCESS_COLOR,
        activebackground=styles.SUCCESS_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=15,
        relief="flat",
        cursor="hand2",
        command=lambda: employee_form.open_form(dash, refresh_dashboard),
    ).pack(side="left", padx=5, ipady=4)

    tk.Button(
        button_frame,
        text="✎ Edit Employee",
        bg=styles.WARNING_COLOR,
        activebackground=styles.WARNING_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=15,
        relief="flat",
        cursor="hand2",
        command=edit_employee,
    ).pack(side="left", padx=5, ipady=4)

    tk.Button(
        button_frame,
        text="✕ Delete Employee",
        bg=styles.DANGER_COLOR,
        activebackground=styles.DANGER_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=15,
        relief="flat",
        cursor="hand2",
        command=delete_employee,
    ).pack(side="left", padx=5, ipady=4)

    tk.Button(
        button_frame,
        text="⬇ Export CSV",
        bg=styles.INFO_COLOR,
        activebackground=styles.INFO_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=15,
        relief="flat",
        cursor="hand2",
        command=export.export_to_csv,
    ).pack(side="left", padx=5, ipady=4)

    tk.Button(
        button_frame,
        text="📊 Department Chart",
        bg=styles.PURPLE_COLOR,
        activebackground=styles.PURPLE_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=18,
        relief="flat",
        cursor="hand2",
        command=charts.show_department_chart,
    ).pack(side="left", padx=5, ipady=4)

    tk.Button(
        button_frame,
        text="✖ Exit",
        bg=styles.GRAY_COLOR,
        activebackground=styles.GRAY_HOVER,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        width=10,
        relief="flat",
        cursor="hand2",
        command=dash.destroy,
    ).pack(side="right", padx=5, ipady=4)

    refresh_dashboard()
    dash.mainloop()


if __name__ == "__main__":
    open_dashboard()
