# API Testing & CI/CD Pipeline Documentation

## Overview

This project includes comprehensive unit tests and a complete GitHub Actions CI/CD pipeline to ensure code quality, security, and reliability.

## Local Testing Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running Tests Locally

#### Run all tests:
```bash
pytest
```

#### Run tests with verbose output:
```bash
pytest -v
```

#### Run tests with coverage report:
```bash
pytest --cov=api_project --cov-report=html --cov-report=term
```

#### Run specific test file:
```bash
pytest test_api_project.py -v
```

#### Run specific test:
```bash
pytest test_api_project.py::TestUserAPI::test_create_user_success -v
```

#### Run tests with different Python versions (using tox):
```bash
pip install tox
tox
```

### Understanding the Tests

The test suite (`test_api_project.py`) includes:

#### TestUserAPI Class
- **test_create_user_success**: Verifies successful user creation with proper response
- **test_create_user_with_missing_data**: Tests behavior when incomplete data is provided
- **test_get_all_users_success**: Verifies retrieval of all users
- **test_get_all_users_empty**: Tests response when no users exist
- **test_get_user_by_id_success**: Verifies successful retrieval of a specific user
- **test_get_user_by_id_not_found**: Tests 404 response for non-existent user
- **test_update_user_success**: Verifies successful user update
- **test_update_user_not_found**: Tests update of non-existent user
- **test_delete_user_success**: Verifies successful user deletion
- **test_delete_user_not_found**: Tests deletion of non-existent user
- **test_post_wrong_method**: Tests HTTP method validation

#### TestAPIEdgeCases Class
- **test_create_user_with_special_characters**: Tests handling of special characters
- **test_create_user_with_negative_age**: Tests boundary condition handling
- **test_get_user_with_invalid_id_format**: Tests invalid URL parameter handling

## GitHub Actions CI/CD Pipeline

### Pipeline Overview

The `.github/workflows/ci-cd.yml` workflow automatically runs on:
- **Push** to `main` or `develop` branches
- **Pull Requests** to `main` or `develop` branches

### Pipeline Jobs

#### 1. **test** Job
- Runs tests on Python 3.8, 3.9, 3.10, and 3.11
- Steps:
  - Check out code
  - Set up Python environment with caching
  - Install dependencies
  - Run flake8 linting (syntax checking)
  - Run pytest with coverage reporting
  - Upload coverage to Codecov
  - Generate coverage badge
  - Archive test results

#### 2. **code-quality** Job
- Runs code quality tools
- Tools used:
  - **black**: Code formatting
  - **isort**: Import sorting
  - **pylint**: Code analysis (minimum score: 7.0)

#### 3. **security-scan** Job
- Runs security vulnerability scans
- Tools used:
  - **bandit**: Python security issues detector
  - **safety**: Dependency vulnerability checker

#### 4. **build-docker** Job
- Builds Docker image on successful tests (main branch only)
- Runs Docker container tests
- Available for Docker deployment

#### 5. **notify** Job
- Final notification job
- Reports overall pipeline status

### Workflow Triggers and Conditions

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

### Setting Up Codecov Integration (Optional)

1. Go to [Codecov.io](https://codecov.io)
2. Connect your GitHub repository
3. Coverage reports will automatically upload
4. Add badge to README: `![codecov](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO/branch/main/graph/badge.svg)`

## Test Coverage

Current test coverage includes:
- ✅ All CRUD operations (Create, Read, Update, Delete)
- ✅ Success scenarios
- ✅ Error handling (404 Not Found)
- ✅ Edge cases (special characters, invalid input)
- ✅ HTTP method validation
- ✅ Empty result handling

### Improving Coverage

To check coverage locally and see which lines aren't tested:
```bash
pytest --cov=api_project --cov-report=html
open htmlcov/index.html  # On macOS
# or
start htmlcov/index.html  # On Windows
```

## Mocking Database Connections

Tests use `unittest.mock` to mock MySQL database connections. This ensures:
- Tests run without requiring a database server
- Tests are fast and isolated
- Tests are reproducible in any environment

Example of mocking:
```python
@patch('api_project.get_db_connection')
def test_create_user_success(self, mock_db):
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 1
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn
    
    # Test code here
```

## Adding New Tests

When adding new endpoints:

1. Create a new test method in `TestUserAPI` or appropriate test class
2. Use the `@patch('api_project.get_db_connection')` decorator
3. Mock cursor and connection objects
4. Make request with `self.client.get/post/put/delete()`
5. Assert response status code and content
6. Assert database methods were called correctly

Example:
```python
@patch('api_project.get_db_connection')
def test_new_endpoint(self, mock_db):
    # Setup mocks
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn
    
    # Test
    response = self.client.get('/new-endpoint')
    
    # Assert
    self.assertEqual(response.status_code, 200)
```

## Docker Support

### Build Docker Image
```bash
docker build -t api-app:latest .
```

### Run Tests in Docker
```bash
docker run --rm api-app:latest python -m pytest test_api_project.py -v
```

## Deployment

### Prerequisites for Deployment
- ✅ All tests passing
- ✅ Code quality checks passing
- ✅ Security scans passed
- ✅ Coverage report generated

### Deployment to Production
The CI/CD pipeline builds Docker images on successful tests to the `main` branch, ready for deployment.

## Troubleshooting

### Tests Failing Locally
1. Ensure Python version is 3.8+
2. Install all dependencies: `pip install -r requirements.txt`
3. Clear pytest cache: `pytest --cache-clear`
4. Check database connection settings (not needed for unit tests)

### GitHub Actions Job Failing
1. Check the "Actions" tab in GitHub repository
2. Review the failed job logs
3. Verify all dependencies are in `requirements.txt`
4. Ensure code changes didn't break imports

### Coverage Reports Not Uploading
1. Verify Codecov integration is enabled
2. Check that `CODECOV_TOKEN` is set (for private repos)
3. Review Codecov logs in GitHub Actions output

## Best Practices

1. **Always run tests locally before pushing:**
   ```bash
   pytest -v --cov=api_project
   ```

2. **Write tests for new features:**
   - One test per test method
   - Use descriptive test names
   - Include docstrings

3. **Keep tests isolated:**
   - Each test should be independent
   - Use mocking for external dependencies
   - Clean up after tests

4. **Monitor coverage trends:**
   - Aim for >80% code coverage
   - Review coverage reports after merges

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Flask Testing Documentation](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Contact

For questions or issues with the tests, please:
1. Check the test documentation
2. Review the failing test
3. Check GitHub Actions logs
4. Create an issue in the repository
