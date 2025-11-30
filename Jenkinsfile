pipeline {
    agent any

    environment {
        // Your Webex room ID (this looks correct from your log)
        WEBEX_ROOM_ID = '6d089b90-c051-11f0-b550-a16ba4dd4e16'
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
                // Run Trivy; don't fail the build here, enforce policy in next stage
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
                // Get the final status of the build
                def status = currentBuild.currentResult

                // Pull the Webex bot token from Jenkins credentials
                withCredentials([string(credentialsId: 'webex-bot-token', variable: 'WEBEX_BOT_TOKEN')]) {
                    // Pass data to the shell via env vars to avoid Groovy interpolation issues
                    withEnv([
                        "WEBEX_BOT_TOKEN=${WEBEX_BOT_TOKEN}",
                        "PIPELINE_STATUS=${status}"
                    ]) {
                        sh '''
                            python3 scripts/send_webex_notification.py \
                                "$WEBEX_ROOM_ID" \
                                "$PIPELINE_STATUS" \
                                "$BUILD_NUMBER" \
                                "$JOB_NAME" \
                                "$BUILD_URL"
                        '''
                    }
                }
            }
        }
    }
}
