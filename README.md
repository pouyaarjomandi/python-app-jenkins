# python-app-jenkins

A simple FastAPI application with a fully automated CI/CD pipeline using Jenkins and Docker.

## Overview

This project demonstrates a complete CI/CD pipeline that automatically tests, builds, and deploys a Python FastAPI application using Jenkins running in Docker.

## Tech Stack

- **Python** + **FastAPI** — REST API
- **Docker** — containerization
- **Jenkins** — CI/CD pipeline
- **Docker Hub** — image registry

## Project Structure

```
python-app-jenkins/
├── main.py               # FastAPI application
├── test_main.py          # pytest tests
├── requirements.txt      # Python dependencies
├── Dockerfile            # App container definition
└── Jenkinsfile           # CI/CD pipeline definition
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Returns app info (env, version) |
| GET | `/health` | Health check |
| GET | `/items/{item_id}` | Get item by ID |

## CI/CD Pipeline

The Jenkins pipeline runs the following stages automatically:

```
Checkout → Run Tests → Build Image → Push to Docker Hub → Deploy
```

1. **Checkout** — clones the repository from GitHub
2. **Run Tests** — creates a Python venv and runs pytest
3. **Build Docker Image** — builds and tags the image with the build number
4. **Push to Docker Hub** — pushes both versioned and `latest` tags
5. **Deploy** — stops the old container and runs the new one

## Getting Started

### Prerequisites

- Docker + Docker Compose
- Jenkins (see setup below)

### Run the App Locally

```bash
docker pull pouyaaj/python-app-jenkins:latest
docker run -d -p 8000:8000 pouyaaj/python-app-jenkins:latest
```

App will be available at `http://localhost:8000`

### Jenkins Setup

```bash
mkdir jenkins_home
sudo chown -R 501:20 jenkins_home
docker compose up -d
```

Jenkins will be available at `http://localhost:8080`

### Run Tests Locally

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/pytest -v
```

## Docker Hub

Image is available at: [pouyaaj/python-app-jenkins](https://hub.docker.com/r/pouyaaj/python-app-jenkins)
