# Complete CI/CD Pipeline Setup Guide
## Jenkins + Docker + GitHub

---

## Prerequisites

- Ubuntu/Linux server (or Windows with WSL)
- GitHub account
- Git installed
- Internet connection

---

## Step 1: Install Docker

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
docker-compose --version

# Restart session
newgrp docker
```

---

## Step 2: Install Jenkins

```bash
# Run Jenkins in Docker
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(which docker):/usr/bin/docker \
  jenkins/jenkins:lts

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

**Copy the password** - You'll need it in Step 3

---

## Step 3: Setup Jenkins

### 3.1 Access Jenkins
- Open browser: `http://localhost:8080`
- Paste the admin password
- Click **Continue**

### 3.2 Install Plugins
- Select **Install suggested plugins**
- Wait for installation to complete

### 3.3 Create Admin User
- Username: `admin`
- Password: `your-password`
- Full name: `Your Name`
- Email: `your-email@example.com`
- Click **Save and Continue**

### 3.4 Jenkins URL
- Keep default: `http://localhost:8080/`
- Click **Save and Finish**
- Click **Start using Jenkins**

---

## Step 4: Install Required Jenkins Plugins

### 4.1 Navigate to Plugin Manager
```
Dashboard → Manage Jenkins → Manage Plugins → Available
```

### 4.2 Search and Install:
- ☑ **Docker Pipeline**
- ☑ **Git**
- ☑ **GitHub Integration**
- ☑ **Pipeline**

### 4.3 Install
- Click **Install without restart**
- Wait for completion

---

## Step 5: Configure Docker in Jenkins

### 5.1 Give Jenkins Docker Permissions
```bash
# Enter Jenkins container
docker exec -it -u root jenkins bash

# Install Docker CLI (if not already)
apt-get update
apt-get install -y docker.io

# Give permissions
chmod 666 /var/run/docker.sock

# Exit container
exit
```

### 5.2 Restart Jenkins
```bash
docker restart jenkins
```

---

## Step 6: Push Code to GitHub

### 6.1 Initialize Git (if not done)
```bash
cd "e:\Projects (2)\ML Projects\AI-Agent"
git init
git add .
git commit -m "Initial commit"
```

### 6.2 Create GitHub Repository
1. Go to https://github.com
2. Click **New repository**
3. Name: `AI-Agent`
4. Click **Create repository**

### 6.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/AI-Agent.git
git branch -M main
git push -u origin main
```

---

## Step 7: Create Jenkins Pipeline Job

### 7.1 Create New Job
```
Dashboard → New Item
```

### 7.2 Configure Job
- **Name**: `email-agent-pipeline`
- **Type**: Select **Pipeline**
- Click **OK**

### 7.3 Configure Pipeline

#### General Section:
- ☑ **GitHub project**
- Project url: `https://github.com/YOUR_USERNAME/AI-Agent`

#### Build Triggers:
- ☑ **Poll SCM**
- Schedule: `H/5 * * * *` (checks every 5 minutes)

#### Pipeline Section:
- **Definition**: Pipeline script from SCM
- **SCM**: Git
- **Repository URL**: `https://github.com/YOUR_USERNAME/AI-Agent.git`
- **Credentials**: Click **Add** → **Jenkins**

##### Add GitHub Credentials:
```
Kind: Username with password
Username: YOUR_GITHUB_USERNAME
Password: YOUR_GITHUB_TOKEN (not password!)
ID: github-credentials
Description: GitHub Credentials
```

**To create GitHub token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select scopes: `repo` (all)
4. Copy token

- **Branch**: `*/main`
- **Script Path**: `Jenkinsfile`

### 7.4 Save
Click **Save**

---

## Step 8: Configure Jenkins Node Label

### 8.1 Configure Built-In Node
```
Dashboard → Manage Jenkins → Manage Nodes and Clouds → Built-In Node → Configure
```

### 8.2 Add Label
- **Labels**: `docker`
- Click **Save**

---

## Step 9: Verify Jenkinsfile

Ensure `Jenkinsfile` exists in your project root with this content:

```groovy
pipeline {
    agent { label 'docker' }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'docker build -t email-agent-backend:${BUILD_NUMBER} .'
                    sh 'docker tag email-agent-backend:${BUILD_NUMBER} email-agent-backend:latest'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'docker build -t email-agent-frontend:${BUILD_NUMBER} .'
                    sh 'docker tag email-agent-frontend:${BUILD_NUMBER} email-agent-frontend:latest'
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            sh 'docker system prune -f'
        }
    }
}
```

---

## Step 10: Run Your First Build

### 10.1 Trigger Build
```
Dashboard → email-agent-pipeline → Build Now
```

### 10.2 Monitor Build
- Click on build number (e.g., #1)
- Click **Console Output**
- Watch the build progress

### 10.3 Expected Output
```
Started by user admin
Checking out git https://github.com/YOUR_USERNAME/AI-Agent.git
Building backend...
Building frontend...
Deploying...
Finished: SUCCESS
```

---

## Step 11: Setup Automatic Builds (Optional)

### Option A: GitHub Webhook (Recommended)

#### 11.1 Make Jenkins Accessible
If Jenkins is on localhost, use **ngrok**:
```bash
# Install ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# Run ngrok
ngrok http 8080
```

Copy the **Forwarding URL** (e.g., `https://abc123.ngrok.io`)

#### 11.2 Configure GitHub Webhook
1. GitHub Repository → **Settings** → **Webhooks** → **Add webhook**
2. **Payload URL**: `https://abc123.ngrok.io/github-webhook/`
3. **Content type**: `application/json`
4. **Which events**: Just the push event
5. ☑ Active
6. Click **Add webhook**

#### 11.3 Update Jenkins Job
```
email-agent-pipeline → Configure → Build Triggers
```
- ☑ **GitHub hook trigger for GITScm polling**
- Click **Save**

### Option B: Poll SCM (Already Configured)
Jenkins checks GitHub every 5 minutes for changes

---

## Step 12: Test the Pipeline

### 12.1 Make a Code Change
```bash
# Edit a file
echo "# Test change" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main
```

### 12.2 Watch Jenkins
- Jenkins will automatically detect the change
- Build will start within 5 minutes (or immediately with webhook)
- Monitor in **Console Output**

---

## Step 13: Verify Deployment

### 13.1 Check Running Containers
```bash
docker ps
```

You should see:
- `email-agent-backend`
- `email-agent-frontend`
- `email-agent-db_service`

### 13.2 Test Application
```bash
# Test backend
curl http://localhost:8001/api/health/

# Test frontend
curl http://localhost:3000/
```

---

## Pipeline Flow Diagram

```
┌─────────────┐
│   GitHub    │
│  (Push Code)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Jenkins   │
│ (Detects    │
│  Change)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Checkout   │
│    Code     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Build Backend│
│   Docker    │
│   Image     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Build Frontend│
│   Docker    │
│   Image     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Deploy    │
│docker-compose│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Application │
│   Running   │
└─────────────┘
```

---

## Troubleshooting

### Build Fails: "docker: command not found"
```bash
docker exec -it -u root jenkins bash
apt-get update && apt-get install -y docker.io
chmod 666 /var/run/docker.sock
exit
docker restart jenkins
```

### Build Fails: "Permission denied"
```bash
sudo chmod 666 /var/run/docker.sock
docker restart jenkins
```

### GitHub Authentication Failed
- Verify GitHub token has `repo` permissions
- Regenerate token if expired
- Update credentials in Jenkins

### Port Already in Use
```bash
# Check what's using port 8080
sudo lsof -i :8080

# Kill the process or change Jenkins port
docker run -p 9090:8080 ...
```

### Jenkins Container Stopped
```bash
docker start jenkins
```

---

## Advanced Configuration

### Email Notifications
```groovy
post {
    success {
        emailext (
            subject: "Build Success: ${env.JOB_NAME}",
            body: "Build ${env.BUILD_NUMBER} succeeded",
            to: "your-email@example.com"
        )
    }
    failure {
        emailext (
            subject: "Build Failed: ${env.JOB_NAME}",
            body: "Build ${env.BUILD_NUMBER} failed",
            to: "your-email@example.com"
        )
    }
}
```

### Slack Notifications
1. Install **Slack Notification** plugin
2. Configure Slack workspace
3. Add to Jenkinsfile:
```groovy
post {
    success {
        slackSend (
            color: 'good',
            message: "Build Successful: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        )
    }
}
```

### Parallel Builds
```groovy
stage('Build') {
    parallel {
        stage('Backend') {
            steps {
                dir('backend') {
                    sh 'docker build -t backend .'
                }
            }
        }
        stage('Frontend') {
            steps {
                dir('frontend') {
                    sh 'docker build -t frontend .'
                }
            }
        }
    }
}
```

---

## Security Best Practices

1. ✅ Use GitHub tokens, not passwords
2. ✅ Store secrets in Jenkins credentials
3. ✅ Enable HTTPS for Jenkins (use reverse proxy)
4. ✅ Restrict Jenkins access (firewall rules)
5. ✅ Regular Jenkins updates
6. ✅ Use `.gitignore` for sensitive files

---

## Maintenance

### Update Jenkins
```bash
docker pull jenkins/jenkins:lts
docker stop jenkins
docker rm jenkins
# Run docker run command again from Step 2
```

### View Jenkins Logs
```bash
docker logs jenkins
docker logs -f jenkins  # Follow logs
```

### Backup Jenkins
```bash
docker exec jenkins tar -czf /tmp/jenkins-backup.tar.gz /var/jenkins_home
docker cp jenkins:/tmp/jenkins-backup.tar.gz ./jenkins-backup.tar.gz
```

---

## Summary

✅ **Installed**: Docker, Jenkins
✅ **Configured**: Jenkins plugins, credentials, node labels
✅ **Created**: GitHub repository, Jenkins pipeline job
✅ **Setup**: Automatic builds on code push
✅ **Deployed**: Application using docker-compose

**Result**: Every code push to GitHub automatically builds and deploys your application!

---

## Next Steps

- Add automated testing stage
- Implement staging/production environments
- Add code quality checks (SonarQube)
- Set up monitoring (Prometheus/Grafana)
- Implement rollback mechanism
