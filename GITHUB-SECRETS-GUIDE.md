# 🔐 GitHub Secrets Setup - Detailed Guide

## What Are GitHub Secrets?

GitHub Secrets are encrypted variables that store sensitive information (passwords, tokens, API keys) securely. They're:
- ✅ **Encrypted** - Hidden from public view
- ✅ **Masked** - Never shown in logs
- ✅ **Secure** - Only used in workflows
- ✅ **Repository-specific** - Only your repo can access them

---

## 📋 What You'll Need

Before adding secrets, gather these credentials:

### 1. AWS Credentials (2 items)

**What:** Your AWS Access Key ID and Secret Access Key

**Where to get them:**
1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Users** in left sidebar
3. Click your username (e.g., "janani")
4. Go to **Security credentials** tab
5. Scroll to **Access keys**
6. Click **Create access key**
   - Select **Command Line Interface (CLI)**
   - Click **Next**
   - Click **Create access key**
7. You'll see:
   - **Access Key ID** - starts with `AKIA...`
   - **Secret Access Key** - a long string

**⚠️ IMPORTANT:** Copy both values now. You can't see the Secret Key again!

### 2. Docker Hub Credentials (2 items)

**What:** Your Docker Hub username and access token

**Where to get them:**
1. Go to [Docker Hub](https://hub.docker.com)
2. Click your profile icon (top right)
3. Click **Account settings**
4. Click **Security** in left menu
5. Click **New Access Token**
   - Name: `github-actions-token`
   - Access permissions: Select `Read, Write, Delete`
   - Click **Generate**
6. Copy the token displayed
   - **Token** - long alphanumeric string
   - **Username** - your docker username

---

## 🚀 Step-by-Step: Add GitHub Secrets

### STEP 1: Go to Your GitHub Repository

1. Open [GitHub](https://github.com)
2. Log in with your account
3. Go to your repository: `https://github.com/YOUR_USERNAME/app_api`

**Example:**
```
https://github.com/janani/app_api
```

---

### STEP 2: Open Settings

1. Click the **Settings** tab at the top
   
   ```
   ┌─────────────────────────────────────┐
   │ Code  Pull Requests  Issues  Wiki   │
   │ Settings  Insights  ...             │
   └─────────────────────────────────────┘
        Click here ↑
   ```

---

### STEP 3: Navigate to Secrets

1. In left sidebar, click **Secrets and variables**

   ```
   Left Sidebar:
   ├── General
   ├── Collaborators
   ├── Secrets and variables    ← Click here
   │   ├── Actions
   │   ├── Dependabot
   │   └── Codespaces
   └── ...
   ```

2. Click **Actions** submenu

   ```
   Secrets and variables
   ├── Actions           ← Click here
   ├── Dependabot
   └── Codespaces
   ```

**Full path:** Settings → Secrets and variables → Actions

---

### STEP 4: Create First Secret - AWS_ACCESS_KEY_ID

1. Click **New repository secret** button

   ```
   ┌────────────────────────────────┐
   │ "New repository secret" button │
   └────────────────────────────────┘
   ```

2. **Name field:** Type exactly:
   ```
   AWS_ACCESS_KEY_ID
   ```

3. **Secret field:** Paste your AWS Access Key ID
   ```
   Example: AKIA2HMQF7UORUR7WUR6
   ```

4. Click **Add secret** button

   ```
   ┌─────────────────────┐
   │ Add secret (button) │
   └─────────────────────┘
   ```

**Result:**
```
✅ AWS_ACCESS_KEY_ID secret added
```

---

### STEP 5: Create Second Secret - AWS_SECRET_ACCESS_KEY

1. Click **New repository secret** button again

2. **Name field:** Type exactly:
   ```
   AWS_SECRET_ACCESS_KEY
   ```

3. **Secret field:** Paste your AWS Secret Access Key
   ```
   Example: G9M2RTTzC2Qsa/Uf2sRVZhoekauV6bbOhnBP7lvY
   ```

4. Click **Add secret** button

**Result:**
```
✅ AWS_SECRET_ACCESS_KEY secret added
```

---

### STEP 6: Create Third Secret - DOCKER_HUB_USERNAME

1. Click **New repository secret** button

2. **Name field:** Type exactly:
   ```
   DOCKER_HUB_USERNAME
   ```

3. **Secret field:** Your Docker Hub username
   ```
   Example: janani
   ```

4. Click **Add secret** button

**Result:**
```
✅ DOCKER_HUB_USERNAME secret added
```

---

### STEP 7: Create Fourth Secret - DOCKER_HUB_TOKEN

1. Click **New repository secret** button

2. **Name field:** Type exactly:
   ```
   DOCKER_HUB_TOKEN
   ```

3. **Secret field:** Your Docker Hub access token
   ```
   Example: dckr_pat_xyz123...
   ```

4. Click **Add secret** button

**Result:**
```
✅ DOCKER_HUB_TOKEN secret added
```

---

## 🎯 Final Result

After all 4 secrets are added, you should see:

```
Repository secrets

✅ AWS_ACCESS_KEY_ID
✅ AWS_SECRET_ACCESS_KEY
✅ DOCKER_HUB_USERNAME
✅ DOCKER_HUB_TOKEN
```

All 4 secrets listed with ✅ checkmarks.

---

## 📸 Visual Guide

### Settings Tab Location
```
GitHub Repository Page
├── Code
├── Issues
├── Pull requests
├── Actions
└── Settings  ← Click here
    └── Dropdown with more options
```

### Secrets Page Layout
```
┌─────────────────────────────────────────┐
│ Repository secrets                      │
├─────────────────────────────────────────┤
│                                         │
│ [New repository secret button]          │
│                                         │
│ Repository secrets (4)                  │
│ ─────────────────────────────────────   │
│ ✅ AWS_ACCESS_KEY_ID                    │
│    (Updated 2 min ago)                  │
│                                         │
│ ✅ AWS_SECRET_ACCESS_KEY                │
│    (Updated 2 min ago)                  │
│                                         │
│ ✅ DOCKER_HUB_USERNAME                  │
│    (Updated 1 min ago)                  │
│                                         │
│ ✅ DOCKER_HUB_TOKEN                     │
│    (Updated just now)                   │
└─────────────────────────────────────────┘
```

---

## 🔍 How to Find Each Secret

### AWS Credentials

**Location:** AWS IAM Console

```
1. Go to https://console.aws.amazon.com/iam/
2. Click "Users" (left sidebar)
3. Click your username
4. Tab: "Security credentials"
5. Section: "Access keys"
6. "Create access key"
   
Two values appear:
- Access Key ID (AKIA...)
- Secret Access Key (long string)
```

**Example:**
```
Access Key ID: AKIA2HMQF7UORUR7WUR6
Secret Access Key: G9M2RTTzC2Qsa/Uf2sRVZhoekauV6bbOhnBP7lvY
```

### Docker Hub Credentials

**Location:** Docker Hub Settings

```
1. Go to https://hub.docker.com
2. Click profile icon (top right)
3. "Account settings"
4. "Security" (left menu)
5. "New Access Token"
   
Fill in:
- Description: github-actions-token
- Access permissions: Read, Write, Delete ✓
- Click "Generate"
   
Two values appear:
- Username: (your docker username)
- Token: dckr_pat_xyz...
```

**Example:**
```
Username: janani
Token: dckr_pat_1234567890abcdef
```

---

## ✅ Verification

### How to Verify Secrets Are Added

1. Go to Settings → Secrets and variables → Actions
2. You should see **all 4 secrets** listed:
   - ✅ AWS_ACCESS_KEY_ID
   - ✅ AWS_SECRET_ACCESS_KEY
   - ✅ DOCKER_HUB_USERNAME
   - ✅ DOCKER_HUB_TOKEN

### Test Secrets in Workflow

When you push code, GitHub Actions will use these secrets:

```
✅ GitHub Actions detects secrets
✅ Pulls values from repository secrets
✅ Uses them in workflow (hidden from logs)
✅ Deletes values after workflow completes
```

**In logs, you'll see:**
```
*** is not recognized
(Secrets are masked/hidden)
```

---

## 🔐 Security Best Practices

### ✅ DO:
- ✅ Keep secret values confidential
- ✅ Rotate credentials every 90 days
- ✅ Use strong passwords (20+ characters)
- ✅ Enable MFA on all accounts
- ✅ Immediately revoke compromised keys

### ❌ DON'T:
- ❌ Share secrets via email/chat
- ❌ Commit secrets to git repository
- ❌ Print secrets in logs
- ❌ Use same password for multiple services
- ❌ Leave access keys lying around

---

## 🚨 If You Made a Mistake

### Secret Added Incorrectly?

1. Click the secret name
2. Click **Update secret**
3. Enter correct value
4. Click **Save**

### Secret Exposed?

1. **IMMEDIATELY** revoke the exposed key:

**For AWS:**
```
1. Go to AWS IAM Console
2. Click Users → Your user
3. Security credentials tab
4. Find the exposed key
5. Click "Deactivate" or "Delete"
6. Create a NEW access key
7. Update GitHub secret with new key
```

**For Docker Hub:**
```
1. Go to Docker Hub Security
2. Find the exposed token
3. Click "Delete"
4. Create a NEW token
5. Update GitHub secret with new token
```

---

## ⚙️ How Secrets Are Used in Workflow

In your `.github/workflows/deploy.yml`, secrets are used like:

```yaml
- name: Login to Amazon ECR
  uses: aws-actions/configure-aws-credentials@v2
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

The `${{ secrets.AWS_ACCESS_KEY_ID }}` syntax:
- Looks up the secret value
- Injects it into the workflow
- **Hides it from logs** (masked with ***)

---

## 📊 Secret Status Check

After adding secrets, here's what you should see:

```
Repository
├── Settings
│   └── Secrets and variables
│       └── Actions
│           ├── New repository secret (button)
│           │
│           └── Repository secrets (4 total)
│               ├── ✅ AWS_ACCESS_KEY_ID
│               │    Updated: 5 minutes ago
│               │
│               ├── ✅ AWS_SECRET_ACCESS_KEY
│               │    Updated: 5 minutes ago
│               │
│               ├── ✅ DOCKER_HUB_USERNAME
│               │    Updated: 3 minutes ago
│               │
│               └── ✅ DOCKER_HUB_TOKEN
│                    Updated: 2 minutes ago
```

---

## 🎯 Summary

| Secret | Value | Source |
|--------|-------|--------|
| `AWS_ACCESS_KEY_ID` | `AKIA...` | AWS IAM Console |
| `AWS_SECRET_ACCESS_KEY` | Long string | AWS IAM Console |
| `DOCKER_HUB_USERNAME` | Your username | Docker Hub Profile |
| `DOCKER_HUB_TOKEN` | `dckr_pat_...` | Docker Hub Security |

---

## 🚀 Next Steps

After adding all 4 secrets:

1. ✅ Secrets added to GitHub
2. → Go to [CI-CD-SETUP.md](CI-CD-SETUP.md)
3. → Follow "Step 2: Configure AWS ECS"
4. → Then push code to trigger workflow

---

## 📞 Troubleshooting

### Workflow Says "Secret not found"

**Cause:** Secret name doesn't match in workflow

**Solution:**
- Check spelling (must be exact match)
- Example: `AWS_ACCESS_KEY_ID` (not `aws_access_key_id`)

### Workflow Fails with "Invalid credentials"

**Cause:** Wrong value in secret

**Solution:**
- Verify value:
  - AWS_ACCESS_KEY_ID starts with `AKIA`
  - AWS_SECRET_ACCESS_KEY is long string (not your master password!)
  - Docker token starts with `dckr_pat_`

### Can't See Secret Value

**This is expected!** GitHub hides secret values for security.

You can only:
- ✅ Update the value
- ✅ Delete the secret
- ❌ View the value (hidden after creation)

---

## ✨ Complete!

You've successfully:
- ✅ Added AWS credentials
- ✅ Added Docker Hub credentials
- ✅ Secured sensitive data
- ✅ Enabled GitHub Actions automation

**Your secrets are now safe and ready to use!** 🎉

---

**Last Updated:** April 12, 2026
**Version:** 1.0.0
**Status:** ✅ Complete
