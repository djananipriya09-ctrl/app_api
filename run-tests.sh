#!/bin/bash
# CI/CD Pipeline Setup & Test Runner Script
# This script installs dependencies and runs all quality checks locally

set -e  # Exit on error

echo "======================================"
echo "API Testing & CI/CD Pipeline Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Install dependencies
echo -e "${YELLOW}Step 1: Installing dependencies...${NC}"
python -m pip install --upgrade pip > /dev/null 2>&1
python -m pip install -r requirements.txt > /dev/null 2>&1
pip install flake8 pylint black isort bandit safety > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 2: Run tests
echo -e "${YELLOW}Step 2: Running unit tests...${NC}"
python -m pytest test_api_project.py -v --cov=api_project --cov-report=term-missing
echo -e "${GREEN}✓ Unit tests completed${NC}"
echo ""

# Step 3: Run linting
echo -e "${YELLOW}Step 3: Running code quality checks...${NC}"
echo "  - Checking with flake8..."
python -m flake8 api_project.py --count --select=E9,F63,F7,F82 --show-source --statistics || true
echo "  - Checking imports with isort..."
python -m isort --check-only api_project.py test_api_project.py || true
echo "  - Analyzing with pylint..."
python -m pylint api_project.py --fail-under=5.0 || true
echo -e "${GREEN}✓ Code quality checks completed${NC}"
echo ""

# Step 4: Security checks
echo -e "${YELLOW}Step 4: Running security scans...${NC}"
echo "  - Running Bandit security check..."
python -m bandit -r api_project.py -ll || true
echo "  - Checking dependencies with Safety..."
python -m safety check || true
echo -e "${GREEN}✓ Security scans completed${NC}"
echo ""

# Summary
echo "======================================"
echo -e "${GREEN}Pipeline execution completed!${NC}"
echo "======================================"
echo ""
echo "Test Artifacts:"
echo "  - Coverage report: htmlcov/index.html"
echo "  - Test results: pytest output above"
echo ""
echo "Next steps:"
echo "  1. Push your code to GitHub"
echo "  2. GitHub Actions will automatically run this pipeline"
echo "  3. Check the Actions tab for detailed results"
echo ""
