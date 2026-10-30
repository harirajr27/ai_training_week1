import json

import pytest
from fastapi.testclient import TestClient
from src.main import JSON_PATH, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    mock_data = [
        {"name": "Leanne Graham", "department": "Engineering", "salary": "75000"},
        {"name": "Ervin Howell", "department": "Design", "salary": "45000"},
    ]
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(mock_data, f, indent=4)
    yield
    if JSON_PATH.exists():
        JSON_PATH.unlink()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_all_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_create_employee_success():
    payload = {"name": "Ravi Kumar", "department": "IT", "salary": 60000}
    response = client.post("/employees", json=payload)
    assert response.status_code == 201


def test_get_employee_not_found():
    response = client.get("/employees/Ravi")
    assert response.status_code == 404


def test_create_employee_invalid_salary():
    payload = {"name": "Suresh", "department": "HR", "salary": -5}
    response = client.post("/employees", json=payload)
    assert response.status_code == 422


def test_create_employee_empty_name():
    payload = {"name": "", "department": "Finance", "salary": 50000}
    response = client.post("/employees", json=payload)
    assert response.status_code == 422
