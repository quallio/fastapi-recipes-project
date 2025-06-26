# FastAPI Recipes Project

Backend API for managing recipes using FastAPI, PostgreSQL, Docker, and Poetry.

## 🚀 Getting Started

These instructions will get your development environment up and running.

### 📦 Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 🛠️ Build and Run the Project

```bash
# Build the Docker image
docker-compose build

# Run the containers in detached mode
docker-compose up -d

```

This will start:

- A FastAPI app running on http://localhost:8000
- A PostgreSQL database on port 5432

### 🧪 Test API Endpoints

You can test the available endpoints using Swagger UI:

- Open http://localhost:8000/docs in your browser.

### 🛑 Stop the Containers

To stop and remove all containers, networks, and volumes:

```bash
# Stop the containers
docker-compose down

```