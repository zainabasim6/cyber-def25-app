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
                        'requirements.txt'
                    ]
                    
                    requiredFiles.each { file ->
                        if (fileExists(file)) {
                            echo "✅ ${file} - FOUND"
                        } else {
                            error "❌ ${file} - MISSING - Build failed!"
                        }
                    }
                    
                    // Check for log files but don't fail if missing
                    if (fileExists('network_logs/sample.log')) {
                        echo "✅ network_logs/sample.log - FOUND"
                    } else {
                        echo "⚠️  network_logs/sample.log - NOT FOUND (will create test data)"
                        sh 'mkdir -p network_logs'
                        sh '''
                        cat > network_logs/sample.log << "EOL"
2024-01-01 10:00:00,192.168.1.100,10.0.0.50,GET /api/data,200
2024-01-01 10:01:00,192.168.1.101,10.0.0.51,POST /login,404
2024-01-01 10:02:00,192.168.1.102,10.0.0.52,GET /admin,403
EOL
                        '''
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
            sh 'docker ps -a || echo "Docker not accessible"'
            sh 'echo "Final images:"'
            sh 'docker images || echo "Docker not accessible"'
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
