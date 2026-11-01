import psycopg2

from src.database import get_db_connection
from src.schemas import EmployeeCreate, EmployeeUpdate


def create_employee(employee: EmployeeCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Parameterized query to avoid SQL injection
        cursor.execute(
            """
            INSERT INTO employees (name, email, department, salary) 
            VALUES (%s, %s, %s, %s) RETURNING id, name, email, department, salary;
            """,
            (employee.name, employee.email, employee.department, employee.salary),
        )
        row = cursor.fetchone()
        conn.commit()
        return row
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return "UNIQUE_VIOLATION"
    finally:
        cursor.close()
        conn.close()


def get_all_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, department, salary FROM employees;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_employee_by_id(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, email, department, salary FROM employees WHERE id = %s;",
        (employee_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def update_employee(employee_id: int, employee: EmployeeUpdate):
    # Fetch existing data first to handle partial updates
    existing = get_employee_by_id(employee_id)
    if not existing:
        return None

    # Merge new fields with existing data if they are omitted in update body
    name = employee.name if employee.name is not None else existing[1]
    email = employee.email if employee.email is not None else existing[2]
    department = employee.department if employee.department is not None else existing[3]
    salary = employee.salary if employee.salary is not None else existing[4]

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE employees 
            SET name = %s, email = %s, department = %s, salary = %s 
            WHERE id = %s RETURNING id, name, email, department, salary;
            """,
            (name, email, department, salary, employee_id),
        )
        row = cursor.fetchone()
        conn.commit()
        return row
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return "UNIQUE_VIOLATION"
    finally:
        cursor.close()
        conn.close()


def delete_employee(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = %s RETURNING id;", (employee_id,))
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return row
