import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import src.database as db_mod
from src.main import app

if hasattr(db_mod, "Base"):
    BaseModelTarget = db_mod.Base
elif hasattr(db_mod, "model"):
    BaseModelTarget = db_mod.model
else:

    class FallbackBase:
        metadata = getattr(db_mod, "metadata", None)

    BaseModelTarget = FallbackBase

# 2. Dynamically find or fallback the database dependency hook name
get_db_dependency = None
for attr_name in ["get_db", "get_session", "db_session", "SessionLocal"]:
    if hasattr(db_mod, attr_name):
        get_db_dependency = getattr(db_mod, attr_name)
        break

# ==============================================================================
# DATABASE & CLIENT FIXTURES (Isolated per-test execution lifecycle)
# ==============================================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Drops and creates all database tables cleanly for every single test to guarantee zero persistence overlap."""
    if BaseModelTarget.metadata is not None:
        BaseModelTarget.metadata.drop_all(bind=engine)
        BaseModelTarget.metadata.create_all(bind=engine)
    yield
    if BaseModelTarget.metadata is not None:
        BaseModelTarget.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Provides an isolated transactional database session context."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Overrides real engine dependencies to isolate testing environments."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    # Apply overrides if a valid matching injection dependency hook target was resolved
    if get_db_dependency is not None:
        app.dependency_overrides[get_db_dependency] = override_get_db

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ==============================================================================
# POSITIVE CRUD TESTS
# ==============================================================================


def test_create_employee(client):
    """Positive: Successfully create a new employee."""
    unique_email = f"john.{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "John Doe",
        "email": unique_email,
        "department": "Engineering",
        "salary": 50000.0,
    }
    response = client.post("/employees/", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]


def test_get_all_employees(client):
    """Positive: Retrieve all employees."""
    email1 = f"alice.{uuid.uuid4().hex[:6]}@example.com"
    email2 = f"bob.{uuid.uuid4().hex[:6]}@example.com"
    client.post(
        "/employees/",
        json={"name": "Alice", "email": email1, "department": "HR", "salary": 60000},
    )
    client.post(
        "/employees/",
        json={"name": "Bob", "email": email2, "department": "IT", "salary": 65000},
    )

    response = client.get("/employees/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_one_employee(client):
    """Positive: Retrieve a single employee by resolving its assigned path payload parameter structure."""
    unique_email = f"charlie.{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "Charlie",
        "email": unique_email,
        "department": "Sales",
        "salary": 70000,
    }
    created_resp = client.post("/employees/", json=payload)
    assert created_resp.status_code in [200, 201]
    created = created_resp.json()

    # Check alternate potential keys to get database primary key identifier dynamically
    emp_id = created.get("id") or created.get("employee_id") or created.get("email")

    response = client.get(f"/employees/{emp_id}")
    if response.status_code == 422:
        # If integer paths raise structural errors, route through query param fallback strings instead
        response = client.get(f"/employees/?id={emp_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Charlie"


def test_update_employee(client):
    """Positive: Partially or fully update an employee record."""
    unique_email = f"david.{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "David",
        "email": unique_email,
        "department": "Marketing",
        "salary": 55000,
    }
    created_resp = client.post("/employees/", json=payload)
    assert created_resp.status_code in [200, 201]
    created = created_resp.json()
    emp_id = created.get("id") or created.get("employee_id") or created.get("email")

    update_payload = {
        "name": "David Smith",
        "email": unique_email,
        "department": "Marketing",
        "salary": 58000,
    }
    response = client.put(f"/employees/{emp_id}", json=update_payload)
    if response.status_code == 422:
        response = client.put(f"/employees/?id={emp_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["name"] == "David Smith"


def test_delete_employee(client):
    """Positive: Delete an employee from the system."""
    unique_email = f"eve.{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "Eve",
        "email": unique_email,
        "department": "Finance",
        "salary": 80000,
    }
    created_resp = client.post("/employees/", json=payload)
    assert created_resp.status_code in [200, 201]
    created = created_resp.json()
    emp_id = created.get("id") or created.get("employee_id") or created.get("email")

    delete_response = client.delete(f"/employees/{emp_id}")
    if delete_response.status_code == 422:
        delete_response = client.delete(f"/employees/?id={emp_id}")

    assert delete_response.status_code in [200, 202, 204]


# ==============================================================================
# NEGATIVE VALIDATION TESTS
# ==============================================================================


def test_create_employee_invalid_email(client):
    """Negative: Fails with a 422 error due to invalid email structure."""
    payload = {
        "name": "Wrong Email",
        "email": "plain-text-string",
        "department": "QA",
        "salary": 45000,
    }
    response = client.post("/employees/", json=payload)
    assert response.status_code == 422


def test_create_employee_negative_salary(client):
    """Negative: Fails with a 422 error because salary is not greater than 0 (gt=0)."""
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "department": "QA",
        "salary": -500.0,
    }
    response = client.post("/employees/", json=payload)
    assert response.status_code == 422


def test_create_employee_missing_name(client):
    """Negative: Fails when required 'name' field is absent."""
    payload = {"email": "no.name@example.com", "department": "QA", "salary": 50000.0}
    response = client.post("/employees/", json=payload)
    assert response.status_code == 422


def test_create_employee_duplicate_email(client):
    """Negative: Rejects creation when the email registry constraint triggers."""
    unique_email = f"same.{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "User Unique",
        "email": unique_email,
        "department": "Design",
        "salary": 50000,
    }

    first_resp = client.post("/employees/", json=payload)
    assert first_resp.status_code in [200, 201]

    response = client.post("/employees/", json=payload)
    assert response.status_code in [400, 409]


def test_get_employee_unknown_id(client):
    """Negative: Querying a non-existent database key returns a 404 Not Found."""
    response = client.get("/employees/99999")
    if response.status_code == 422:
        # Fallback to string uuid key if routing layer uses custom validation mapping rules
        response = client.get(f"/employees/{uuid.uuid4()}")
    assert response.status_code == 404
