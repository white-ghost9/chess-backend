import sqlite3
from datetime import datetime
import os

# Database file path (same folder as this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "company.db")

# ==========================================================
# Database Connection
# ==========================================================


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ==========================================================
# Create Tables (Runs only once)
# ==========================================================


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT UNIQUE,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            salary REAL NOT NULL,
            join_date TEXT NOT NULL,
            photo TEXT
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
        """)

    # Default admin account
    cursor.execute("SELECT username FROM admin WHERE username=?", ("admin",))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ("admin", "admin123"),
        )

    conn.commit()
    conn.close()


# ==========================================================
# Generate Employee ID
# ==========================================================


def generate_employee_id():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT emp_id FROM employees ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    if row:
        last_number = int(row[0].replace("EMP", ""))
        return f"EMP{last_number + 1:03d}"

    return "EMP001"


# ==========================================================
# Check Duplicate Employee
# ==========================================================


def employee_exists(email, phone):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM employees WHERE email=? OR phone=?", (email, phone))

    exists = cursor.fetchone() is not None

    conn.close()
    return exists


# ==========================================================
# Add Employee
# ==========================================================


def add_employee(name, department, position, email, phone, salary, join_date, photo):
    if employee_exists(email, phone):
        return False, "An employee with this email or phone number already exists."

    conn = connect()
    cursor = conn.cursor()

    emp_id = generate_employee_id()

    try:
        cursor.execute(
            """
            INSERT INTO employees
            (emp_id, name, department, position, email, phone, salary, join_date, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                emp_id,
                name,
                department,
                position,
                email,
                phone,
                salary,
                join_date,
                photo,
            ),
        )

        conn.commit()
        return True, f"Employee {emp_id} added successfully."

    except sqlite3.IntegrityError:
        return False, "Duplicate email or phone number."

    finally:
        conn.close()


# ==========================================================
# Get All Employees
# ==========================================================


def get_all_employees():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, emp_id, name, department, position,
               email, phone, salary, join_date, photo
        FROM employees
        ORDER BY id DESC
        """)

    rows = cursor.fetchall()

    conn.close()
    return rows


# ==========================================================
# Search Employee
# ==========================================================


def search_employee(keyword):
    conn = connect()
    cursor = conn.cursor()

    keyword_pattern = f"%{keyword}%"

    cursor.execute(
        """
        SELECT id, emp_id, name, department, position,
               email, phone, salary, join_date, photo
        FROM employees
        WHERE emp_id LIKE ?
           OR name LIKE ?
           OR department LIKE ?
           OR position LIKE ?
           OR email LIKE ?
           OR phone LIKE ?
        ORDER BY id DESC
        """,
        (
            keyword_pattern,
            keyword_pattern,
            keyword_pattern,
            keyword_pattern,
            keyword_pattern,
            keyword_pattern,
        ),
    )

    rows = cursor.fetchall()

    conn.close()
    return rows


# ==========================================================
# Update Employee
# ==========================================================


def update_employee(
    emp_id, name, department, position, email, phone, salary, join_date, photo
):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM employees
        WHERE (email=? OR phone=?)
          AND emp_id != ?
        """,
        (email, phone, emp_id),
    )

    if cursor.fetchone():
        conn.close()
        return False, "Another employee already uses this email or phone number."

    cursor.execute(
        """
        UPDATE employees
        SET name=?,
            department=?,
            position=?,
            email=?,
            phone=?,
            salary=?,
            join_date=?,
            photo=?
        WHERE emp_id=?
        """,
        (
            name,
            department,
            position,
            email,
            phone,
            salary,
            join_date,
            photo,
            emp_id,
        ),
    )

    conn.commit()
    conn.close()

    return True, "Employee updated successfully."


# ==========================================================
# Delete Employee
# ==========================================================


def delete_employee(emp_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))

    conn.commit()
    conn.close()
    return True, "Employee deleted successfully."


# ==========================================================
# Dashboard Statistics
# ==========================================================


def get_statistics():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT department) FROM employees")
    departments = cursor.fetchone()[0]

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("SELECT COUNT(*) FROM employees WHERE join_date=?", (today,))

    joined_today = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "departments": departments,
        "today": joined_today,
    }


# ==========================================================
# Validate Admin Login
# ==========================================================


def validate_admin(username, password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM admin WHERE username=? AND password=?", (username, password)
    )

    valid = cursor.fetchone() is not None

    conn.close()

    return valid


if __name__ == "__main__":
    create_tables()
    print("Database initialized successfully.")
