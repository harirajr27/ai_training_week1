
from fastapi import FastAPI, HTTPException, status

from src import crud
from src.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate

app = FastAPI(title="Employee CRUD API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


# 1. POST /employees (Create an employee)
@app.post(
    "/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED
)
def create_employee_endpoint(employee: EmployeeCreate):
    result = crud.create_employee(employee)
    if result == "UNIQUE_VIOLATION":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An employee with this email already exists",
        )

    return {
        "id": result[0],
        "name": result[1],
        "email": result[2],
        "department": result[3],
        "salary": float(result[4]),
    }


# 2. GET /employees (List all employees)
@app.get("/employees", response_model=list[EmployeeResponse])
def get_all_employees_endpoint():
    rows = crud.get_all_employees()
    employees = []
    for row in rows:
        employees.append(
            {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "department": row[3],
                "salary": float(row[4]),
            }
        )
    return employees


# 3. GET /employees/{id} (Retrieve one employee)
@app.get("/employees/{id}", response_model=EmployeeResponse)
def get_employee_endpoint(id: int):
    row = crud.get_employee_by_id(id)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "department": row[3],
        "salary": float(row[4]),
    }


# 4. PUT /employees/{id} (Update an employee)
@app.put("/employees/{id}", response_model=EmployeeResponse)
def update_employee_endpoint(id: int, employee: EmployeeUpdate):
    result = crud.update_employee(id, employee)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    if result == "UNIQUE_VIOLATION":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An employee with this email already exists",
        )
    return {
        "id": result[0],
        "name": result[1],
        "email": result[2],
        "department": result[3],
        "salary": float(result[4]),
    }


# 5. DELETE /employees/{id} (Remove an employee)
@app.delete("/employees/{id}", status_code=status.HTTP_200_OK)
def delete_employee_endpoint(id: int):
    result = crud.delete_employee(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )
    return {"message": f"Employee with id {id} deleted successfully"}
