pipeline {
    agent any

    environment {
        // Replace with your real Webex room ID
        WEBEX_ROOM_ID = '6d089b90-c051-11f0-b550-a16ba4dd4e16'

        // Jenkins credential: kind "Secret text", id "webex-bot-token"
        WEBEX_BOT_TOKEN = credentials('N2VjYzI2YjMtZWQxNC00YjAxLWJiZTQtZWY3Yjc4M2YzMDc5YzllNmM5NTEtYjI4_P0A1_13494cac-24b4-4f89-8247-193cc92a7636')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies (for scripts)') {
            steps {
                sh 'pip install --user requests'
            }
        }

        stage('Build & Test') {
            steps {
                sh 'echo "No automated tests yet - add pytest here if you want"'
                // Example: sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t secure-app:${BUILD_NUMBER} .'
            }
        }

        stage('Security Scan - Trivy') {
            steps {
                // --exit-code 0 so Trivy itself doesn't fail the build; we handle policy in evaluate_trivy.py
                sh '''
                    trivy image --format json \
                      --output trivy-report.json \
                      secure-app:${BUILD_NUMBER} || true
                '''
            }
        }

        stage('Evaluate Security Policy') {
            steps {
                sh 'python scripts/evaluate_trivy.py trivy-report.json'
            }
        }

        stage('Deploy (Mock)') {
            when {
                expression {
                    // Only run if pipeline is still SUCCESS
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh 'echo "Mock deploy: secure-app:${BUILD_NUMBER} (no real deployment)"'
                // You could instead run the container here:
                // sh 'docker run -d -p 5000:5000 secure-app:${BUILD_NUMBER}'
            }
        }
    }

    post {
        always {
            script {
                def status = currentBuild.currentResult
                sh """
                    WEBEX_BOT_TOKEN="${WEBEX_BOT_TOKEN}" \
                    python scripts/send_webex_notification.py \
                        "${WEBEX_ROOM_ID}" \
                        "${status}" \
                        "${BUILD_NUMBER}" \
                        "${JOB_NAME}" \
                        "${BUILD_URL}"
                """
            }
        }
    }
}
