# Jenkins CI/CD Pipeline Setup

## Prerequisites

- Jenkins installed
- Docker installed on Jenkins server
- Docker Hub account
- GitHub repository

## Step 1: Install Jenkins

### Using Docker:
```bash
docker run -d \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins \
  jenkins/jenkins:lts
```

### Get Initial Admin Password:
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Access Jenkins at: http://localhost:8080

## Step 2: Install Required Plugins

1. Go to **Manage Jenkins** → **Manage Plugins**
2. Install these plugins:
   - Docker Pipeline
   - Git
   - Pipeline
   - GitHub Integration (optional)

## Step 3: Configure Docker Hub Credentials

1. **Manage Jenkins** → **Manage Credentials**
2. Click **(global)** → **Add Credentials**
3. Configure:
   - Kind: Username with password
   - Username: Your Docker Hub username
   - Password: Your Docker Hub password
   - ID: `dockerhub-credentials`
   - Description: Docker Hub Credentials

## Step 4: Create Pipeline Job

1. **New Item** → Enter name: `email-agent-pipeline`
2. Select **Pipeline** → Click OK
3. Configure:

### General:
- ☑ GitHub project
- Project url: `https://github.com/your-username/AI-Agent`

### Build Triggers:
- ☑ GitHub hook trigger for GITScm polling (if using webhooks)
- ☑ Poll SCM: `H/5 * * * *` (check every 5 minutes)

### Pipeline:
- Definition: **Pipeline script from SCM**
- SCM: **Git**
- Repository URL: `https://github.com/your-username/AI-Agent.git`
- Credentials: Add your GitHub credentials
- Branch: `*/main`
- Script Path: `Jenkinsfile`

4. Click **Save**

## Step 5: Configure Environment Variables

### Option A: In Jenkinsfile (Not Recommended for Secrets)
Already configured in the Jenkinsfile

### Option B: Jenkins Credentials (Recommended)
1. **Manage Jenkins** → **Manage Credentials**
2. Add each secret:
   - DATABASE_URL
   - EMAIL
   - APP_PASSWORD
   - GROQ_API_KEY
   - GEMINI_API_KEY

Then update Jenkinsfile to use credentials:
```groovy
environment {
    DATABASE_URL = credentials('database-url')
    EMAIL = credentials('email')
    APP_PASSWORD = credentials('app-password')
    GROQ_API_KEY = credentials('groq-api-key')
}
```

## Step 6: Configure GitHub Webhook (Optional)

### In GitHub Repository:
1. Go to **Settings** → **Webhooks** → **Add webhook**
2. Configure:
   - Payload URL: `http://your-jenkins-server:8080/github-webhook/`
   - Content type: `application/json`
   - Events: Just the push event
   - ☑ Active

### Make Jenkins Accessible:
If Jenkins is on localhost, use ngrok:
```bash
ngrok http 8080
```
Use the ngrok URL in webhook

## Step 7: Update Docker Images

In `Jenkinsfile`, replace:
```groovy
DOCKER_IMAGE_BACKEND = 'your-username/email-agent-backend'
DOCKER_IMAGE_FRONTEND = 'your-username/email-agent-frontend'
```

With your actual Docker Hub username.

## Step 8: Run Pipeline

1. Go to your pipeline job
2. Click **Build Now**
3. Monitor the build in **Console Output**

## Pipeline Stages

1. **Checkout** - Clone repository
2. **Build Backend** - Build backend Docker image
3. **Build Frontend** - Build frontend Docker image
4. **Push to Registry** - Push images to Docker Hub
5. **Deploy** - Deploy using docker-compose

## Troubleshooting

### Docker Permission Denied:
```bash
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Cannot Connect to Docker:
```bash
# Mount Docker socket in Jenkins container
docker run -v /var/run/docker.sock:/var/run/docker.sock ...
```

### Build Fails:
- Check Console Output for errors
- Verify Docker Hub credentials
- Ensure Jenkinsfile is in repository root
- Check Docker is running

## Advanced Configuration

### Multi-Branch Pipeline:
For multiple branches (dev, staging, prod):
1. Create **Multibranch Pipeline**
2. Add branch sources
3. Jenkins auto-discovers branches with Jenkinsfile

### Parallel Builds:
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

### Email Notifications:
```groovy
post {
    success {
        emailext (
            subject: "Build Successful: ${env.JOB_NAME}",
            body: "Build ${env.BUILD_NUMBER} succeeded",
            to: "your-email@example.com"
        )
    }
}
```

## Testing the Pipeline

1. Make a code change
2. Commit and push to GitHub
3. Jenkins automatically triggers build
4. Monitor progress in Jenkins UI
5. Verify deployment

## Production Deployment

For production, modify the Deploy stage:
```groovy
stage('Deploy to Production') {
    when {
        branch 'main'
    }
    steps {
        sshagent(['production-server-ssh']) {
            sh '''
                ssh user@production-server "
                    cd /app/AI-Agent &&
                    git pull &&
                    docker-compose down &&
                    docker-compose up -d
                "
            '''
        }
    }
}
```

## Monitoring

- **Build History**: View all builds
- **Console Output**: Detailed logs
- **Blue Ocean**: Modern UI for pipelines
- **Metrics**: Build duration, success rate

## Security Best Practices

1. ✅ Use credentials manager for secrets
2. ✅ Enable CSRF protection
3. ✅ Use HTTPS for Jenkins
4. ✅ Restrict job permissions
5. ✅ Regular Jenkins updates
6. ✅ Scan Docker images for vulnerabilities

## Next Steps

- Set up automated testing
- Add code quality checks (SonarQube)
- Implement blue-green deployment
- Add rollback mechanism
- Set up monitoring and alerts
