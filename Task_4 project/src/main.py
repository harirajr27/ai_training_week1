import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
JSON_PATH = Path("employees.json")


class Employee(BaseModel):
    name: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    salary: float = Field(..., gt=0)


def load_employees() -> list:
    if not JSON_PATH.exists():
        return []
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_employees(employees: list) -> None:
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(employees, f, indent=4)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/employees")
def get_all_employees():
    return load_employees()


@app.get("/employees/{name}")
def get_employee_by_name(name: str):
    employees = load_employees()
    for emp in employees:
        if emp.get("name", "").lower() == name.lower():
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(employee: Employee):
    employees = load_employees()
    new_emp = employee.model_dump()
    new_emp["salary"] = (
        str(int(employee.salary))
        if employee.salary.is_integer()
        else str(employee.salary)
    )
    employees.append(new_emp)
    save_employees(employees)
    return {"message": "Employee created successfully", "employee": new_emp}

