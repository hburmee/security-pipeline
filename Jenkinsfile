pipeline {
    agent any

    environment {
        // Replace with your Webex room ID
        WEBEX_ROOM_ID = '6d089b90-c051-11f0-b550-a16ba4dd4e16'

        // Jenkins credential: "Secret text" with ID 'webex-bot-token'
        WEBEX_BOT_TOKEN = credentials('webex-bot-token')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devsecops-app:${BUILD_NUMBER} .'
            }
        }

        stage('Security Scan - Trivy') {
            steps {
                // Trivy may return non-zero, so we use || true and enforce policy later
                sh '''
                    trivy image \
                      --format json \
                      --output trivy-report.json \
                      devsecops-app:${BUILD_NUMBER} || true
                '''
            }
        }

        stage('Evaluate Security Policy') {
            steps {
                sh 'python3 scripts/evaluate_trivy.py trivy-report.json'
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
                sh 'echo "Mock deploy of devsecops-app:${BUILD_NUMBER} (no real deployment)"'
            }
        }
    }

    post {
        always {
            script {
                def status = currentBuild.currentResult

                // Pass values into env vars so we don't interpolate secrets into the shell
                withEnv([
                    "WEBEX_BOT_TOKEN=${WEBEX_BOT_TOKEN}",
                    "PIPELINE_STATUS=${status}",
                    "PIPELINE_BUILD_NUMBER=${BUILD_NUMBER}",
                    "PIPELINE_JOB_NAME=${JOB_NAME}",
                    "PIPELINE_BUILD_URL=${BUILD_URL}"
                ]) {
                    sh '''
                        python3 scripts/send_webex_notification.py \
                            "$WEBEX_ROOM_ID" \
                            "$PIPELINE_STATUS" \
                            "$PIPELINE_BUILD_NUMBER" \
                            "$PIPELINE_JOB_NAME" \
                            "$PIPELINE_BUILD_URL"
                    '''
                }
            }
        }
    }
}
