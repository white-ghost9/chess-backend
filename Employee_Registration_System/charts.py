# charts.py

import matplotlib.pyplot as plt
from tkinter import messagebox
from . import database


def show_department_chart():
    """Display a professional bar chart of employees per department."""
    try:
        employees = database.get_all_employees()

        if not employees:
            messagebox.showwarning(
                "No Data",
                "There are no employee records available for chart generation.",
            )
            return

        # Count employees by department
        department_count = {}

        for emp in employees:
            department = emp[3]  # Department column
            department_count[department] = department_count.get(department, 0) + 1

        departments = list(department_count.keys())
        counts = list(department_count.values())

        plt.figure(figsize=(10, 6))

        bars = plt.bar(
            departments,
            counts,
            color="#2563EB",
            edgecolor="black",
        )

        plt.title(
            "Employees per Department",
            fontsize=16,
            fontweight="bold",
        )

        plt.xlabel("Department", fontsize=12)
        plt.ylabel("Number of Employees", fontsize=12)

        plt.grid(axis="y", linestyle="--", alpha=0.4)

        # Display value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.05,
                str(int(height)),
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror(
            "Chart Error",
            f"Failed to generate department chart.\n\n{e}",
        )
