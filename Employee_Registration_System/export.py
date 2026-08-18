# export.py
# Provides functionality to export employee records to a CSV file.

import csv
import os
from datetime import datetime
from tkinter import messagebox, filedialog

import database


def export_to_csv():
    """Export all employee records from the database to a CSV file."""
    employees = database.get_all_employees()

    if not employees:
        messagebox.showwarning(
            "No Data",
            "There are no employee records available to export.",
        )
        return

    # Default filename with current date/time
    default_filename = f"employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    file_path = filedialog.asksaveasfilename(
        title="Save Employee Records",
        defaultextension=".csv",
        initialfile=default_filename,
        filetypes=[
            ("CSV files", "*.csv"),
            ("All Files", "*.*"),
        ],
    )

    if not file_path:
        return  # User cancelled

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Header row
            writer.writerow(
                [
                    "Employee ID",
                    "Name",
                    "Department",
                    "Position",
                    "Email",
                    "Phone",
                    "Salary",
                    "Join Date",
                ]
            )

            # Data rows
            for emp in employees:
                writer.writerow(
                    [
                        emp[1],  # emp_id
                        emp[2],  # name
                        emp[3],  # department
                        emp[4],  # position
                        emp[5],  # email
                        emp[6],  # phone
                        emp[7],  # salary
                        emp[8],  # join_date
                    ]
                )

        messagebox.showinfo(
            "Export Successful",
            f"Employee records exported successfully to:\n{os.path.basename(file_path)}",
        )

    except Exception as e:
        messagebox.showerror(
            "Export Error",
            f"Failed to export employee records.\n\n{e}",
        )
