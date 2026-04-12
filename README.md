# Flask User API - Complete Setup & Deployment Guide

A production-ready Flask REST API with JWT authentication, AWS RDS integration, Docker containerization, and health check endpoints for AWS Load Balancer.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Local Setup & Development](#local-setup--development)
- [Testing](#testing)
- [Docker Setup](#docker-setup)
- [AWS Setup](#aws-setup)
- [GitHub Integration](#github-integration)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- ✅ **RESTful API** - Complete CRUD operations for users
- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **AWS RDS MySQL** - Cloud database with SSL encryption
- ✅ **Health Check Endpoint** - AWS Load Balancer compatibility
- ✅ **Docker Support** - Containerized deployment
- ✅ **Unit Tests** - 24 comprehensive tests with mocking
- ✅ **Code Quality** - Flake8 linting, PEP 8 compliant
- ✅ **CI/CD Ready** - GitHub Actions integration
- ✅ **AWS ECS** - Scalable container orchestration

---

## 🔧 Prerequisites

### System Requirements
- **Windows/Linux/macOS**
- **Python 3.8+**
- **Docker Desktop** (for containerization)
- **Git** (for version control)
- **AWS Account** (for cloud deployment)

### Required AWS Services
- RDS MySQL instance
- ECR (Elastic Container Registry)
- ECS (Elastic Container Service)
- Load Balancer

---

## 📁 Project Structure

```
app_api/
├── api_project.py           # Main Flask application
├── test_api_project.py      # Unit tests (24 tests)
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── pytest.ini               # Pytest configuration
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── global-bundle.pem        # AWS RDS SSL certificate
└── README.md                # This file
```

---

## 🚀 Local Setup & Development

### Step 1: Clone Repository

```bash
cd C:\Users\DELL\OneDrive\Documents
git clone https://github.com/YOUR_USERNAME/app_api.git
cd app_api
```

### Step 2: Create Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy template
Copy-Item .env.example .env

# Edit .env with your AWS RDS details
```

**Fill in these values from AWS RDS:**
```dotenv
DB_HOST=janani-db.chiyiwsmu58m.eu-north-1.rds.amazonaws.com
DB_USER=admin
DB_PASSWORD=your_password
DB_NAME=jananidb
DB_PORT=3306
DB_SSL_CA=./global-bundle.pem
SECRET_KEY=your_secret_key_here
```

### Step 5: Download AWS RDS SSL Certificate

```bash
curl -o global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

### Step 6: Create Database & Tables

```bash
mysql -h janani-db.chiyiwsmu58m.eu-north-1.rds.amazonaws.com -P 3306 -u admin -p --ssl-mode=VERIFY_IDENTITY --ssl-ca=./global-bundle.pem -e "CREATE DATABASE IF NOT EXISTS jananidb; CREATE TABLE IF NOT EXISTS jananidb.users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT);"
```

### Step 7: Run Application Locally

```bash
python -m flask run --host=0.0.0.0 --port=5000
```

**Output:**
```
 * Running on http://0.0.0.0:5000
```

---

## 🧪 Testing

### Run All Tests

```bash
python -m pytest test_api_project.py -v
```

**Expected Output:**
```
24 passed in 1.42s
```

### Run Specific Test

```bash
python -m pytest test_api_project.py::TestHealthCheck -v
```

### Code Quality Check

```bash
python -m flake8 api_project.py test_api_project.py --max-line-length=100
```

### Test Coverage

```bash
pytest --cov=api_project test_api_project.py
```

---

## 🐳 Docker Setup

### Step 1: Build Docker Image

```bash
docker build -t janani/myapp:latest .
```

### Step 2: Test Locally

```bash
docker run -p 5000:5000 --env-file .env janani/myapp:latest
```

### Step 3: Verify Container

```bash
curl http://localhost:5000/health
```

---

## ☁️ AWS Setup

### Step 1: Configure AWS Credentials

```powershell
aws configure

# Enter your AWS credentials:
AWS Access Key ID: AKIA...
AWS Secret Access Key: ...
Default region: eu-north-1
Default output format: json
```

### Step 2: Create/Verify RDS MySQL

1. Go to [AWS RDS Console](https://console.aws.amazon.com/rds/)
2. Click **Databases** → **Create database**
   - Engine: MySQL 8.0
   - DB instance identifier: `janani-db`
   - Master username: `admin`
   - Master password: (create strong password)
   - Publicly accessible: **Yes**
3. Note the **Endpoint** (e.g., `janani-db.xxx.eu-north-1.rds.amazonaws.com`)
4. Update `.env` with endpoint

### Step 3: Configure Security Group

1. RDS instance → **Connectivity & security**
2. Click security group link
3. **Inbound rules** → **Edit**
4. Add rule:
   - Type: MySQL/Aurora
   - Port: 3306
   - Source: 0.0.0.0/0 (or your IP)
5. Click **Save**

### Step 4: Push to AWS ECR

```powershell
# Get AWS account ID and region
$AWS_ACCOUNT_ID = "703066406173"
$AWS_REGION = "eu-north-1"
$ECR_REPO = "app-api"

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Tag image
docker tag janani/myapp:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

# Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest
```

### Step 5: Create ECS Cluster & Service

1. Go to [AWS ECS Console](https://console.aws.amazon.com/ecs/)
2. Click **Clusters** → **Create cluster**
   - Name: `app-cluster`
   - Infrastructure: EC2/Fargate
3. Click **Create**

### Step 6: Create Task Definition

1. **Task Definitions** → **Create new task definition**
   - Name: `app-task`
   - Container name: `app`
   - Image: `{AWS_ACCOUNT_ID}.dkr.ecr.eu-north-1.amazonaws.com/app-api:latest`
   - Port mappings: 5000:5000
   - Environment variables:
     ```
     DB_HOST=janani-db.chiyiwsmu58m.eu-north-1.rds.amazonaws.com
     DB_USER=admin
     DB_PASSWORD=your_password
     DB_NAME=jananidb
     DB_PORT=3306
     DB_SSL_CA=/app/global-bundle.pem
     FLASK_ENV=production
     ```

### Step 7: Create ECS Service

1. **Services** → **Create service**
   - Cluster: `app-cluster`
   - Task definition: `app-task`
   - Desired count: 2
   - Load balancer: Enable
   - Container port: 5000
   - Health check path: `/health`

---

## 🔄 GitHub Integration

### Step 1: Create GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit: Flask API with AWS RDS integration"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/app_api.git
git push -u origin main
```

### Step 2: Add Secrets (for CI/CD)

1. Go to GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`: `eu-north-1`
   - `ECR_REGISTRY`: `{AWS_ACCOUNT_ID}.dkr.ecr.eu-north-1.amazonaws.com`
   - `ECR_REPOSITORY`: `app-api`

### Step 3: GitHub Actions CI/CD

Create `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy to ECS

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest test_api_project.py -v
    
    - name: Run flake8
      run: |
        python -m flake8 api_project.py test_api_project.py --max-line-length=100
    
    - name: Build and push Docker image
      run: |
        aws ecr get-login-password --region ${{ secrets.AWS_REGION }} | docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}
        docker build -t ${{ secrets.ECR_REGISTRY }}/${{ secrets.ECR_REPOSITORY }}:latest .
        docker push ${{ secrets.ECR_REGISTRY }}/${{ secrets.ECR_REPOSITORY }}:latest
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## 📡 API Endpoints

### 1. Health Check (No Auth Required)

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "User API",
  "timestamp": "2026-04-12T12:00:00.000000"
}
```

### 2. Login (Get JWT Token)

```bash
POST /login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login successful"
}
```

### 3. Create User

```bash
POST /users
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "name": "John Doe",
  "age": 30
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 30
}
```

### 4. Get All Users

```bash
GET /users
Authorization: Bearer {TOKEN}
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "age": 30
  }
]
```

### 5. Get User by ID

```bash
GET /users/{id}
Authorization: Bearer {TOKEN}
```

### 6. Update User

```bash
PUT /users/{id}
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "name": "Jane Doe",
  "age": 32
}
```

### 7. Delete User

```bash
DELETE /users/{id}
Authorization: Bearer {TOKEN}
```

---

## 🔐 Security Best Practices

### Credentials Management

✅ **DO:**
- Use `.env` for local development
- Use AWS Secrets Manager for production
- Rotate credentials regularly
- Use strong passwords (20+ characters)

❌ **DON'T:**
- Commit `.env` to git (it's in `.gitignore`)
- Share AWS credentials in chat/email
- Use default passwords
- Expose secrets in Docker images

### Example: Using AWS Secrets Manager

```python
import boto3

secrets_client = boto3.client('secretsmanager', region_name='eu-north-1')
secret = secrets_client.get_secret_value(SecretId='app-api/db-credentials')
db_credentials = json.loads(secret['SecretString'])
```

---

## 🔧 Troubleshooting

### 1. Connection Timeout to RDS

**Cause:** Security group not allowing port 3306

**Solution:**
```bash
# Check endpoint is reachable
Test-NetConnection -ComputerName janani-db.xxx.eu-north-1.rds.amazonaws.com -Port 3306

# Update security group inbound rules to allow MySQL
```

### 2. Database Not Found Error

**Cause:** Database `jananidb` doesn't exist

**Solution:**
```bash
# Create database
mysql -h {RDS_ENDPOINT} -u admin -p -e "CREATE DATABASE jananidb;"
```

### 3. Docker Image Build Fails

**Cause:** Missing dependencies

**Solution:**
```bash
# Rebuild with verbose output
docker build -t janani/myapp:latest . --verbose
```

### 4. ECS Task Not Starting

**Cause:** Invalid environment variables or image not found

**Solution:**
1. Check CloudWatch logs
2. Verify ECR image exists
3. Update task definition with correct environment variables

### 5. JWT Token Expired

**Cause:** Token older than 24 hours

**Solution:**
```bash
# Get new token
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

## 📊 Testing Summary

**Test Suite:** 24+ tests
- ✅ CRUD operations
- ✅ JWT authentication
- ✅ Error handling
- ✅ Health check
- ✅ Edge cases

**Run tests:**
```bash
python -m pytest test_api_project.py -v
```

---

## 📦 Deployment Checklist

- [ ] AWS RDS instance created and running
- [ ] Security group allows MySQL (3306)
- [ ] Database and tables created
- [ ] All environment variables configured
- [ ] Local tests passing
- [ ] Docker image builds successfully
- [ ] Tests passing in Docker container
- [ ] ECR repository created
- [ ] Image pushed to ECR
- [ ] ECS cluster created
- [ ] Task definition created
- [ ] ECS service running
- [ ] Load Balancer health checks passing
- [ ] API endpoints responding
- [ ] GitHub secrets configured
- [ ] CI/CD pipeline working

---

## 🔗 Useful Links

- [Flask Documentation](https://flask.palletsprojects.com/)
- [AWS RDS Guide](https://docs.aws.amazon.com/rds/)
- [Docker Documentation](https://docs.docker.com/)
- [JWT Authentication](https://pyjwt.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)

---

## 👤 Author

Created: April 12, 2026

---

## 📝 License

This project is open source and available under the MIT License.

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Check CloudWatch logs (for AWS deployments)
3. Review error messages in application logs
4. Contact AWS support for infrastructure issues

---

**Last Updated:** April 12, 2026
**Version:** 1.0.0
**Status:** ✅ Production Ready
