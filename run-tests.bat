@echo off
REM CI/CD Pipeline Setup & Test Runner Script for Windows
REM This script installs dependencies and runs all quality checks locally

setlocal enabledelayedexpansion

echo.
echo ======================================
echo API Testing ^& CI/CD Pipeline Setup
echo ======================================
echo.

REM Step 1: Install dependencies
echo [Step 1] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt >nul 2>&1
pip install flake8 pylint black isort bandit safety >nul 2>&1
echo [DONE] Dependencies installed
echo.

REM Step 2: Run tests
echo [Step 2] Running unit tests...
python -m pytest test_api_project.py -v --cov=api_project --cov-report=term-missing
echo [DONE] Unit tests completed
echo.

REM Step 3: Run linting
echo [Step 3] Running code quality checks...
echo   - Checking with flake8...
python -m flake8 api_project.py --count --select=E9,F63,F7,F82 --show-source --statistics
echo   - Checking imports with isort...
python -m isort --check-only api_project.py test_api_project.py
echo   - Analyzing with pylint...
python -m pylint api_project.py --fail-under=5.0
echo [DONE] Code quality checks completed
echo.

REM Step 4: Security checks
echo [Step 4] Running security scans...
echo   - Running Bandit security check...
python -m bandit -r api_project.py -ll
echo   - Checking dependencies with Safety...
python -m safety check
echo [DONE] Security scans completed
echo.

REM Summary
echo ======================================
echo Pipeline execution completed!
echo ======================================
echo.
echo Test Artifacts:
echo   - Coverage report: htmlcov\index.html
echo   - Test results: pytest output above
echo.
echo Next steps:
echo   1. Push your code to GitHub
echo   2. GitHub Actions will automatically run this pipeline
echo   3. Check the Actions tab for detailed results
echo.
pause
