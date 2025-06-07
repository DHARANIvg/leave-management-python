import sqlite3
from datetime import datetime

DB_NAME = "leave_manager.db"
#l..........................................
def connect_db():
    return sqlite3.connect(DB_NAME)
#.................................................
def init_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS leave_balances (
            employee_id INTEGER,
            leave_type TEXT,
            balance INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );

        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            leave_type TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        );
        """)
        conn.commit()
def get_employee_by_name(name):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM employees WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

def add_employee(name, initial_balances):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name) VALUES (?)", (name,))
        emp_id = cursor.lastrowid
        for leave_type, balance in initial_balances.items():
            cursor.execute("INSERT INTO leave_balances (employee_id, leave_type, balance) VALUES (?, ?, ?)",
                           (emp_id, leave_type, balance))
        conn.commit()

def get_leave_balance(emp_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT leave_type, balance FROM leave_balances WHERE employee_id = ?", (emp_id,))
        return dict(cursor.fetchall())

def update_leave_balance(emp_id, leave_type, delta):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE leave_balances
            SET balance = balance + ?
            WHERE employee_id = ? AND leave_type = ?
        """, (delta, emp_id, leave_type))
        conn.commit()

def add_leave_request(emp_id, leave_type, start_date, end_date, status="Pending"):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (emp_id, leave_type, start_date, end_date, status))
        conn.commit()

def get_leave_requests(emp_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT leave_type, start_date, end_date, status
            FROM leave_requests
            WHERE employee_id = ?
            ORDER BY start_date DESC
        """, (emp_id,))
        return cursor.fetchall()

def cancel_leave(emp_id, leave_type, start_date):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE leave_requests
            SET status = 'Cancelled'
            WHERE employee_id = ? AND leave_type = ? AND start_date = ? AND status = 'Approved'
        """, (emp_id, leave_type, start_date))
        conn.commit()

if __name__ == "__main__":
    init_db()
    name = "Alice"
    if not get_employee_by_name(name):
        add_employee(name, {
            "Sick Leave": 5,
            "Annual Leave": 10,
            "Maternity Leave": 0
        })
        print(f"{name} added to the database.")
    else:
        print(f"{name} already exists.")

if __name__ == "__main__":
     init_db()
     name = "Anne"
     if not get_employee_by_name(name):
         add_employee(name, {
             "Sick Leave": 2,
             "Annual Leave": 12,
             "Maternity Leave": 18
         })
         print(f"{name} added to the database.")
     else:
         print(f"{name} already exists.")