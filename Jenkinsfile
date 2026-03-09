pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "pouyaaj/python-app-jenkins"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                    url: 'https://github.com/pouyaarjomandi/python-app-jenkins.git',
                    branch: 'main',
                    credentialsId: 'github-credentials'
                )
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pytest --tb=short
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Deploy') {
            steps {
                sh """
                    docker stop python-app || true
                    docker rm python-app || true
                    docker run -d \
                        --name python-app \
                        -p 8000:8000 \
                        -e APP_ENV=production \
                        -e APP_VERSION=${DOCKER_TAG} \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline موفق بود! Image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }
        failure {
            echo "Pipeline شکست خورد!"
        }
        always {
            sh "docker logout || true"
        }
    }
}
