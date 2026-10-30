# Python Lab Assignment - All Tasks Completed

This repository contains the complete implementation of Tasks 1 through 4, following strict code quality guidelines, testing frameworks, and secure environment setups.

## Folder Structure
- `Task1.py` - Core Python and Class concepts.
- `task2.py` - File handling (CSV, JSON, Excel, PDF) with robust error logging.
- `task3.py` - Safe API traversal and Webhook security with HMAC signatures.
- `Task_4 project/` - Isolated FastAPI service with structured Pydantic validation models.

## How to Set Up and Run the Application

### 1. Installation
Ensure your virtual environment is active, then install all project prerequisites:
```bash
pip install -r requirements.txt
```

### 2. Running the Tasks
- **Task 1:** `python ../Task1.py`
- **Task 2:** `Copy-Item ../employees.csv .; python ../task2.py`
- **Task 3:** `python ../task3.py`

### 3. Execution of FastAPI Test Suite (Task 4)
To execute the automated testing workflow with code coverage tracking, use:
```bash
pytest "Task_4 project/tests/test_main.py" -v --cov="Task_4 project/src"
```
