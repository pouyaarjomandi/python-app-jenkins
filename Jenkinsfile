pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "pouyaaj/python-app-jenkins"
        DOCKER_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = "python-app"
        APP_PORT = "8000"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    set -e
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements-dev.txt
                    ./venv/bin/pytest --tb=short -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -e
                    docker build --pull -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        set -e
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -e
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        --restart unless-stopped \
                        -p ${APP_PORT}:8000 \
                        -e APP_ENV=production \
                        -e APP_VERSION=${DOCKER_TAG} \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    set -e
                    for i in 1 2 3 4 5; do
                        if docker exec ${CONTAINER_NAME} python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)"; then
                            echo "Deployment is healthy."
                            exit 0
                        fi
                        sleep 3
                    done
                    echo "Deployment health check failed."
                    docker logs ${CONTAINER_NAME} || true
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. Image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }
        failure {
            echo "Pipeline failed."
        }
        always {
            sh '''
                docker logout || true
                rm -rf venv || true
            '''
        }
    }
}