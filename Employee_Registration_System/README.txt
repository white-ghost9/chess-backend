Security & setup notes:
- The SQLite database file `company.db` should not be committed. If you need sample data, keep a sanitized `company.db.example` or use `database.py` to initialize.
- To initialize the database on first run, the `database.create_tables()` function will create required tables automatically.
- A `.gitignore` has been added to exclude `*.db`, `__pycache__/`, `.vscode/`, and compiled Python files.
## Security & Setup Notes

* The SQLite database file `company.db` should not be committed. If you need sample data, keep a sanitized `company.db.example` or use `database.py` to initialize.
* To initialize the database on first run, the `database.create_tables()` function will create required tables automatically.
* A `.gitignore` has been added to exclude `*.db`, `__pycache__/`, `.vscode/`, and compiled Python files.
# Employee Management System

## Project Overview

The Employee Management System is a desktop application developed using **Python, Tkinter, and SQLite**. It provides a modern graphical interface for managing employee records, including registration, searching, deletion, data export, and department-wise visualization. The system is designed for educational purposes and small business employee management.

---

## Prerequisites

Before running the project, ensure the following software is installed:

* **Python 3.8 or higher**
* **pip** (Python package manager)

---

## Required Libraries

This project uses the following external libraries:

* **Matplotlib** — for graphical reports
* **Pillow** — for displaying employee photos
* **tkcalendar** — for the date picker

Install them all using:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
Employee_Management_System/
│
├── app.py               # Main application entry point
├── login.py             # Admin login screen
├── dashboard.py         # Employee dashboard
├── employee_form.py     # Add employee form
├── database.py          # SQLite database operations
├── styles.py            # UI colors and fonts
├── export.py            # Export employee records to CSV
├── charts.py            # Department-wise charts
├── company.db           # Auto-created SQLite database
└── README.txt           # Project documentation
```

---

## Running the Application

1. Open **Command Prompt** or **Terminal**.
2. Navigate to the project folder.
3. Run the application:

```bash
python app.py
```

---

## Default Admin Login

Use the following credentials to access the dashboard:

* **Username:** `admin`
* **Password:** `admin123`

---

## Features

* Secure Admin Login
* Add New Employees
* Edit Employee Records
* Search Employees
* Delete Employee Records
* View Employee Details & Photo
* View Employee Dashboard
* Department & Position Management
* Salary and Joining Date Records
* Export Employee Data to CSV
* Department-wise Charts and Statistics
* SQLite Database Integration
* Professional Tkinter User Interface

---

## Technologies Used

* **Python 3**
* **Tkinter** (GUI)
* **SQLite** (Database)
* **Matplotlib** (Charts & Reports)

---

## Notes

* The database file **company.db** is created automatically when the application runs for the first time.
* Ensure all project files remain in the same directory.
* Keep the **assets/** folder (if used for employee photos or icons) inside the project directory.

---

## Author

**MULIYA JENISH M.**

BCA Semester 5

GEETANJALI GROUP OF COLLEGES
