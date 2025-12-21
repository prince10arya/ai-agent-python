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
