# CI/CD Automation Setup Guide

This guide explains how to set up automated deployment to Docker Hub and AWS ECS using GitHub Actions.

## 🔄 Automation Flow

```
Push Code to GitHub
        ↓
    Run Tests & Linting
        ↓
    Build Docker Image
        ↓
  ┌─────┴──────┐
  ↓            ↓
Docker Hub   AWS ECR
        ↓
    Deploy to ECS
        ↓
   Send Notifications
```

---

## 📋 Prerequisites

- GitHub repository
- Docker Hub account
- AWS account (ECR & ECS)
- AWS credentials (Access Key & Secret Key)

---

## ⚙️ Step 1: Set Up GitHub Secrets

GitHub Secrets are encrypted variables used in workflows. They're never shown in logs.

### Navigate to GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

### Add Required Secrets

Add these secrets one by one:

#### AWS Secrets

```
Name: AWS_ACCESS_KEY_ID
Value: AKIA... (from AWS IAM)

---

Name: AWS_SECRET_ACCESS_KEY
Value: ... (from AWS IAM)

---

Name: AWS_REGION
Value: eu-north-1
```

**How to get AWS credentials:**
1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Users** → Your user
3. **Security credentials** tab
4. Click **Create access key**
5. Copy **Access Key ID** and **Secret Access Key**

#### Docker Hub Secrets

```
Name: DOCKER_HUB_USERNAME
Value: your_dockerhub_username

---

Name: DOCKER_HUB_TOKEN
Value: your_dockerhub_token
```

**How to get Docker Hub token:**
1. Go to [Docker Hub](https://hub.docker.com/)
2. Login
3. Click profile icon → **Account settings**
4. Click **Security** → **New Access Token**
5. Copy the token

#### Optional: Slack Notifications

```
Name: SLACK_WEBHOOK_URL
Value: https://hooks.slack.com/services/xxx/yyy/zzz
```

**How to get Slack webhook:**
1. Go to [Slack API](https://api.slack.com/apps)
2. Create New App
3. Navigate to **Incoming Webhooks**
4. Create New Webhook
5. Copy the Webhook URL

---

## 📁 Step 2: Verify Workflow File

Check that `.github/workflows/deploy.yml` exists in your repository:

```
.github/
└── workflows/
    └── deploy.yml
```

---

## 🚀 Step 3: Configure AWS ECS (First Time Only)

### Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name app-cluster --region eu-north-1
```

### Create ECS Task Definition

```bash
aws ecs register-task-definition \
  --family app-task \
  --network-mode awsvpc \
  --container-definitions '[
    {
      "name": "app",
      "image": "703066406173.dkr.ecr.eu-north-1.amazonaws.com/app-api:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DB_HOST",
          "value": "janani-db.chiyiwsmu58m.eu-north-1.rds.amazonaws.com"
        },
        {
          "name": "DB_USER",
          "value": "admin"
        },
        {
          "name": "DB_PORT",
          "value": "3306"
        },
        {
          "name": "DB_NAME",
          "value": "jananidb"
        },
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:eu-north-1:703066406173:secret:db-password"
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:eu-north-1:703066406173:secret:flask-secret-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/app-task",
          "awslogs-region": "eu-north-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]' \
  --cpu 256 \
  --memory 512 \
  --region eu-north-1
```

### Create ECS Service

```bash
aws ecs create-service \
  --cluster app-cluster \
  --service-name app-service \
  --task-definition app-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:eu-north-1:703066406173:targetgroup/app-targets/xxx,containerName=app,containerPort=5000 \
  --region eu-north-1
```

---

## 🔄 Step 4: How Automation Works

### When You Push Code

```bash
git add .
git commit -m "Add new feature"
git push origin main
```

### Workflow Steps (Automatic)

1. **GitHub Actions Triggered**
   - Detects push to `main` branch
   - Starts workflow execution

2. **Run Tests**
   ```
   ✅ Unit tests (24 tests)
   ✅ Flake8 linting
   ✅ Code coverage
   ```

3. **If Tests Pass**
   ```
   ✅ Build Docker image
   ✅ Push to Docker Hub
   ✅ Push to AWS ECR
   ```

4. **Deploy to ECS**
   ```
   ✅ Update task definition
   ✅ Deploy new task
   ✅ Health check verification
   ```

5. **Notify**
   ```
   ✅ Send Slack notification (optional)
   ✅ Update GitHub status
   ```

---

## 📊 Monitor Workflow Execution

### View Workflow Status

1. Go to your GitHub repository
2. Click **Actions** tab
3. See workflow execution status
4. Click on a workflow for details

### What Gets Logged

```
✅ Each step with output
✅ Test results
✅ Build logs
✅ Deployment progress
✅ Error messages (if any)
```

### Example Successful Output

```
✅ Checkout Code
✅ Set up Python
✅ Install Dependencies
✅ Run Unit Tests - 24 passed
✅ Run Flake8 Linting - No issues
✅ Build Docker Image
✅ Push to Docker Hub
✅ Build & Push to AWS ECR
✅ Deploy to ECS
✅ Send Notifications
```

---

## 🐛 Troubleshooting

### Tests Failing

**Check:**
1. Click on "Test & Lint Code" job
2. See which test failed
3. Fix code locally
4. Test locally: `pytest test_api_project.py -v`
5. Push again

### ECR Push Failing

**Cause:** AWS credentials invalid or missing

**Fix:**
```bash
# Verify secrets exist
# Check GitHub Settings → Secrets

# Verify AWS credentials
aws sts get-caller-identity
```

### ECS Deployment Failing

**Cause:** Task definition or service doesn't exist

**Fix:**
```bash
# Create task definition
aws ecs register-task-definition --family app-task ...

# Create service
aws ecs create-service --service-name app-service ...
```

### Docker Hub Push Failing

**Cause:** Invalid credentials or rate limit

**Fix:**
```bash
# Verify credentials
docker login -u {username} -p {password}

# Check Docker Hub for rate limits
```

---

## 📝 Workflow Configuration

### File Location
```
.github/workflows/deploy.yml
```

### Trigger Conditions

**Automatic Deployment to Production:**
- Only on `main` branch
- Only on push (not pull requests)

**Testing on All Changes:**
- All branches
- Both push and pull requests

### Disable Deployment

Edit `.github/workflows/deploy.yml`:

```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

Change to:

```yaml
if: false  # Disable deployment
```

---

## 🔐 Security Best Practices

### Secrets Management

✅ **Never:**
- Print secrets in logs
- Commit secrets to repository
- Share credentials via email/chat

✅ **Always:**
- Use GitHub Secrets for sensitive data
- Rotate credentials regularly
- Use AWS Secrets Manager for runtime secrets

### Example: Secure Secret Usage

```yaml
env:
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

This will never be logged or printed.

---

## 🚀 Advanced Configuration

### Conditional Deployment

Deploy only certain branches:

```yaml
if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop')
```

### Manual Workflow Trigger

Add to workflow:

```yaml
on:
  workflow_dispatch:
```

Then in GitHub > Actions, you can manually trigger the workflow.

### Deploy on Tags

```yaml
on:
  push:
    tags:
      - 'v*'
```

Deploys only when tags like `v1.0.0` are pushed.

---

## 📈 Monitoring & Logging

### View Real-Time Logs

```bash
# GitHub CLI
gh run list -R {owner/repo}
gh run view {run_id} -R {owner/repo}
```

### CloudWatch Logs (ECS)

```bash
aws logs tail /ecs/app-task --follow
```

### Check ECS Task Status

```bash
aws ecs describe-services --cluster app-cluster --services app-service --region eu-north-1
```

---

## 🎯 Success Checklist

- [ ] AWS credentials added to GitHub Secrets
- [ ] Docker Hub credentials added to GitHub Secrets
- [ ] `.github/workflows/deploy.yml` exists in repository
- [ ] ECR repository created (`app-api`)
- [ ] ECS cluster created (`app-cluster`)
- [ ] ECS service created (`app-service`)
- [ ] Task definition created (`app-task`)
- [ ] Tests passing locally
- [ ] Docker builds successfully locally
- [ ] First push to main triggers workflow
- [ ] Workflow completes successfully
- [ ] New image appears in Docker Hub
- [ ] New image appears in ECR
- [ ] ECS service updated with new task
- [ ] Application accessible at load balancer URL

---

## 📞 Quick Reference Commands

### AWS CLI

```bash
# View cluster
aws ecs describe-clusters --clusters app-cluster

# View service
aws ecs describe-services --cluster app-cluster --services app-service

# View task definition
aws ecs describe-task-definition --task-definition app-task

# Update ECS service
aws ecs update-service --cluster app-cluster --service app-service --force-new-deployment

# View logs
aws logs tail /ecs/app-task --follow
```

### Docker Hub

```bash
# Login
docker login

# Push to Docker Hub
docker push {username}/app-api:latest

# View image
docker pull {username}/app-api:latest
```

### GitHub

```bash
# View workflow status
gh run list -R {owner/repo}

# View specific run
gh run view {run_id}

# Check logs
gh run view {run_id} --log
```

---

## 🔗 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Docker Hub API](https://docs.docker.com/docker-hub/api/)

---

**Last Updated:** April 12, 2026
**Version:** 1.0.0
**Status:** ✅ Ready for Production
