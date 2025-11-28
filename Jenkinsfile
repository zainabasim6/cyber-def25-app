pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE_NAME = "malware-detector"
    }
    
    stages {
        stage('Checkout from GitHub') {
            steps {
                echo "🚀 Starting CyberDEF25 Pipeline..."
                checkout scm
                sh 'pwd'
                sh 'ls -la'
            }
        }
        
        stage('Validate Required Files') {
            steps {
                echo "📋 Validating project files..."
                script {
                    def requiredFiles = [
                        'Dockerfile',
                        'docker-compose.yml', 
                        'inference.py',
                        'model.pkl',
                        'requirements.txt',
                        'network_logs/sample.log'
                    ]
                    
                    requiredFiles.each { file ->
                        if (fileExists(file)) {
                            echo "✅ ${file} - FOUND"
                        } else {
                            error "❌ ${file} - MISSING - Build failed!"
                        }
                    }
                    echo "✅ All required files are present!"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "🔨 Building Docker image..."
                sh 'docker build -t $DOCKER_IMAGE_NAME .'
                echo "✅ Docker image built successfully!"
            }
        }
        
        stage('Run Container with Docker Compose') {
            steps {
                echo "🐳 Starting container with Docker Compose..."
                sh 'docker-compose down || true'
                sh 'docker-compose up --build -d'
                sleep(time: 25, unit: 'SECONDS')
                echo "✅ Container is running!"
            }
        }
        
        stage('Check Container Logs') {
            steps {
                echo "📊 Checking container logs..."
                sh 'docker-compose logs --tail=30'
            }
        }
        
        stage('Verify Results') {
            steps {
                echo "✅ Verifying detection results..."
                script {
                    if (fileExists('output/alerts.csv')) {
                        echo "🎉 SUCCESS: Threat detection completed!"
                        sh 'echo "=== ALERTS.CSV CONTENTS ==="'
                        sh 'cat output/alerts.csv'
                        sh 'echo "=== END OF ALERTS ==="'
                    } else {
                        echo "⚠️  No alerts.csv found"
                        sh 'ls -la output/ || echo "Output directory not found"'
                    }
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo "🧹 Cleaning up containers..."
                sh 'docker-compose down || true'
                sh 'docker rmi $DOCKER_IMAGE_NAME || true'
                echo "✅ Cleanup completed!"
            }
        }
    }
    
    post {
        always {
            echo "📈 ===== PIPELINE EXECUTION COMPLETED ====="
            sh 'echo "Final container status:"'
            sh 'docker ps -a'
            sh 'echo "Final images:"'
            sh 'docker images'
        }
        success {
            echo "🎉 🎉 🎉 CYBERDEF25 PIPELINE - SUCCESS! 🎉 🎉 🎉"
            sh 'echo "All stages completed successfully!"'
        }
        failure {
            echo "❌ ❌ ❌ CYBERDEF25 PIPELINE - FAILED! ❌ ❌ ❌"
            sh 'echo "Pipeline execution failed. Check logs above."'
        }
    }
}
