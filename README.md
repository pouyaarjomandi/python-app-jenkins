# python-app-jenkins

A small FastAPI application with a Jenkins-based CI/CD pipeline using Docker and Docker Hub.

## Overview

This project demonstrates a local CI/CD workflow for a Python FastAPI application.

The Jenkins pipeline runs tests, builds a Docker image, pushes it to Docker Hub, deploys the container on the Jenkins host, and verifies the deployment through the `/health` endpoint.

This is a local CI/CD demonstration project. It is not a Kubernetes or cloud deployment.

## Tech Stack

- Python + FastAPI
- pytest
- Docker
- Jenkins
- Docker Hub

## Project Structure

```text
python-app-jenkins/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── Jenkinsfile
├── README.md
├── main.py
├── requirements.txt
├── requirements-dev.txt
└── test_main.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Returns application message, environment, and version |
| GET | `/health` | Health check endpoint |
| GET | `/items/{item_id}` | Returns a sample item by numeric ID |

Example response from `/`:

```json
{
  "message": "Hello from Python!",
  "env": "production",
  "version": "1"
}
```

## Run Tests Locally

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements-dev.txt
./venv/bin/pytest -v
```

## Run with Docker

```bash
docker build -t python-app-jenkins:local .

docker run -d \
  --name python-app-test \
  -p 8000:8000 \
  -e APP_ENV=production \
  -e APP_VERSION=local-test \
  python-app-jenkins:local

curl http://localhost:8000/health

docker stop python-app-test
docker rm python-app-test
```

## Docker Image

The image uses `python:3.11-slim`, runs the application with a non-root user, and includes a Docker health check for the `/health` endpoint.

Runtime dependencies are defined in `requirements.txt`; test dependencies are defined in `requirements-dev.txt`.

## CI/CD Pipeline

The Jenkins pipeline runs:

```text
Checkout → Run Tests → Build Docker Image → Push to Docker Hub → Deploy → Verify Deployment
```

Docker Hub pushes require a Jenkins credential named:

```text
dockerhub-credentials
```

## Docker Hub

[pouyaaj/python-app-jenkins](https://hub.docker.com/r/pouyaaj/python-app-jenkins)

## Companion Project

This project can be used with the companion Jenkins environment:

[jenkins-docker](https://github.com/pouyaarjomandi/jenkins-docker)

The `jenkins-docker` project provides a local Dockerized Jenkins environment with Docker socket access for running this CI/CD pipeline.