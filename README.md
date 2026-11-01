# Mini Employee CRUD API

A production-ready FastAPI application providing full CRUD (Create, Read, Update, Delete) management capabilities for employee databases with data validation and isolated automated tests.

## 🚀 Setup & Installation Steps

### 1. Initialize Virtual Environment
```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate
```

### 2. Install Project Dependencies
```bash
pip install -r requirements.txt
pip install pytest pytest-cov httpx sqlalchemy pre-commit black ruff
```

### 3. Environment Configurations
Create a `.env` file in the root directory and add the following context:
```env
DATABASE_URL=sqlite:///./employees.db
```

### 4. Create Database Tables
```bash
python -m src.scripts.create_tables
```

---

## 🏃‍♂️ How to Run the Application
Start the local development server using Uvicorn:
```bash
uvicorn src.main:app --reload
```
Once initialized, visit the interactive Swagger API documentation page at:
👉 **http://127.0.0**

---

## 🧪 Running Automated Testing and Coverage
Execute the isolated testing lifecycle suite using the required environment targets:
```bash
\$env:PYTHONPATH="." ; pytest --cov=src --cov-report=term-missing
```

---

## 📋 Available API Endpoints List

| HTTP Method | Route Endpoint | Purpose / Functionality |
| :--- | :--- | :--- |
| **POST** | `/employees/` | Creates a new employee record with data validation |
| **GET** | `/employees/` | Retrieves a complete list of all registered employees |
| **GET** | `/employees/{id}` | Retrieves a single employee by their unique identifier |
| **PUT** | `/employees/{id}` | Updates existing metrics for a single employee record |
| **DELETE** | `/employees/{id}` | Permanently drops an employee record from the database |
