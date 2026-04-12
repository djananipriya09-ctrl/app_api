# 🚀 Quick Start: Automated CI/CD Pipeline

## 📝 5-Minute Setup Guide

### Step 1: Add GitHub Secrets (2 minutes)

Go to: **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**

Add these 4 secrets:

```
1. AWS_ACCESS_KEY_ID          → AKIA...
2. AWS_SECRET_ACCESS_KEY      → ... (from AWS IAM)
3. DOCKER_HUB_USERNAME        → your_docker_username
4. DOCKER_HUB_TOKEN          → your_docker_token
```

### Step 2: Configure AWS ECS (First Time Only)

```bash
# Create cluster
aws ecs create-cluster --cluster-name app-cluster --region eu-north-1

# Create task definition
aws ecs register-task-definition --family app-task ...

# Create service
aws ecs create-service --cluster app-cluster --service-name app-service ...
```

### Step 3: Push Code

```bash
git add .
git commit -m "Your changes"
git push origin main
```

### Step 4: Watch Automation ✨

Go to: **GitHub Repository** → **Actions** → Watch workflow execute

```
✅ Tests pass
✅ Docker builds
✅ Pushes to Docker Hub
✅ Pushes to AWS ECR
✅ Deploys to ECS
✅ Done!
```

---

## 🔄 What Happens Automatically

### When You:
```bash
git push origin main
```

### The Pipeline:

1. **Tests Run** (5 seconds)
   - 24 unit tests
   - Flake8 linting
   - Code coverage

2. **Docker Image Built** (30 seconds)
   - Builds image from Dockerfile
   - Runs tests inside container

3. **Push to Docker Hub** (20 seconds)
   - Tags: `latest` and `commit-sha`
   - Updates Docker Hub repository

4. **Push to AWS ECR** (20 seconds)
   - Pushes same image to AWS
   - ECR stores for ECS

5. **Deploy to ECS** (30 seconds)
   - Updates task definition
   - Rolls out new containers
   - Health check passes
   - Old containers removed

6. **Total Time: ~2 minutes** ⏱️

---

## 📊 Pipeline Visualization

```
┌─────────────────────────────────────────┐
│        You Push Code to GitHub          │
└────────────────┬────────────────────────┘
                 │
                 ▼
         ┌──────────────┐
         │  Run Tests   │ ← Fails? Stop here
         └────┬─────────┘
              │
              ▼ (All pass ✅)
      ┌──────────────────┐
      │ Build Docker     │
      │ Image            │
      └────┬─────────────┘
           │
           ▼
    ┌──────────────────┐
    │ Push to Docker   │
    │ Hub              │
    └────┬─────────────┘
         │
         ▼
    ┌──────────────────┐
    │ Push to AWS ECR  │
    └────┬─────────────┘
         │
         ▼
    ┌──────────────────┐
    │ Deploy to ECS    │
    │ (Auto-scale)     │
    └────┬─────────────┘
         │
         ▼
    ✅ Done!
```

---

## 🎯 Key Files

### Workflow File
```
.github/workflows/deploy.yml
```

### Configuration Files
```
- Dockerfile           (Container definition)
- requirements.txt     (Python dependencies)
- pytest.ini          (Test configuration)
- .env.example        (Env variables template)
```

### Source Code
```
- api_project.py      (Flask API)
- test_api_project.py (Unit tests)
```

---

## 🔐 Security

### Secrets (Hidden from logs)
- AWS credentials ✅
- Docker credentials ✅
- Database password ✅

### Never in Logs
- Access keys
- Passwords
- Tokens

---

## ❌ If Something Fails

### Tests Fail
```
→ Fix code locally
→ Run tests: pytest test_api_project.py -v
→ Push again
```

### Docker Build Fails
```
→ Check Dockerfile syntax
→ Build locally: docker build -t test .
→ Fix issues, push again
```

### Docker Hub Push Fails
```
→ Check Docker Hub credentials
→ Verify token hasn't expired
→ Regenerate token if needed
```

### ECR Push Fails
```
→ Check AWS credentials in secrets
→ Verify AWS_REGION is correct
→ Check IAM permissions
```

### ECS Deploy Fails
```
→ Check ECS cluster exists
→ Verify ECS service exists
→ Check task definition is valid
→ Review CloudWatch logs
```

---

## 📱 View Progress

### On GitHub
1. Push code
2. Go to **Actions** tab
3. See workflow running in real-time
4. Click for detailed logs

### Sample Output
```
✅ test (5 sec)
  ✅ Tests passed
  ✅ Linting passed

✅ push-docker-hub (20 sec)
  ✅ Image built
  ✅ Pushed to Docker Hub

✅ push-aws-ecr (20 sec)
  ✅ Image pushed to ECR

✅ deploy-ecs (30 sec)
  ✅ Task definition updated
  ✅ Service updated
  ✅ Deployment successful
```

---

## 🚀 Advanced: Manual Deployments

To manually trigger workflow without pushing code:

1. Go to **Actions** tab
2. Select workflow
3. Click **Run workflow**

This is useful for:
- Redeploying same version
- Testing workflow manually
- Emergency deployments

---

## 📊 Monitoring

### Check Deployment Status

```bash
aws ecs describe-services \
  --cluster app-cluster \
  --services app-service
```

### View Logs

```bash
aws logs tail /ecs/app-task --follow
```

### Check Task Status

```bash
aws ecs list-tasks --cluster app-cluster
```

---

## 🎓 Learning Path

1. **Understand Workflow** → Read `.github/workflows/deploy.yml`
2. **Setup Secrets** → Configure GitHub Secrets
3. **Create ECS Resources** → Set up cluster & service
4. **Push Test Code** → Trigger first workflow
5. **Monitor Execution** → Watch GitHub Actions
6. **Verify Deployment** → Check Docker Hub & ECR
7. **Access Application** → Use load balancer URL

---

## 💡 Tips

✅ **Best Practices:**
- Always run tests locally before pushing
- Use meaningful commit messages
- Tag releases: `git tag v1.0.0 && git push origin v1.0.0`
- Monitor ECS dashboard for issues

❌ **Avoid:**
- Pushing without testing
- Committing secrets
- Disabling tests
- Using weak passwords

---

## 📞 Common Commands

```bash
# Test locally
pytest test_api_project.py -v

# Check code quality
flake8 api_project.py test_api_project.py --max-line-length=100

# Build Docker locally
docker build -t test:latest .

# Push code
git add .
git commit -m "message"
git push origin main

# Check ECS status
aws ecs describe-services --cluster app-cluster --services app-service
```

---

## ✨ Next Steps

1. ✅ Add GitHub Secrets
2. ✅ Create ECS Cluster & Service
3. ✅ Push code to main branch
4. ✅ Watch automation work
5. ✅ Access application from load balancer
6. ✅ Monitor logs in CloudWatch

---

## 🎉 You're All Set!

Your CI/CD pipeline is now automated:
- ✅ Tests run automatically
- ✅ Docker images built automatically
- ✅ Images pushed to Docker Hub automatically
- ✅ Images pushed to AWS ECR automatically
- ✅ ECS service updated automatically
- ✅ Application deployed automatically

**From now on: Push code → Automatic deployment happens! 🚀**

---

**Status:** Ready for Production ✅
**Updated:** April 12, 2026
**Version:** 1.0.0
