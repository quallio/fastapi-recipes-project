# 🍲 FastAPI Recipes API

Production-ready REST API to manage **authors**, **recipes** and **ingredients**  
(Built with FastAPI + PostgreSQL, packaged with Docker, following a clean layered architecture).

---

## ✨ Key Features

| Layer | Responsibility | Folders |
|-------|----------------|---------|
| **Presentation** | HTTP routes & Pydantic DTOs | `app/presentation` |
| **Application**  | Business services & domain rules | `app/application` |
| **Domain**       | SQLAlchemy ORM entities | `app/domain` |
| **Persistence**  | Repositories / DB access | `app/persistence` |

* Full CRUD for **Author**, **Recipe**, **Ingredient**  
* Business checks (unique e-mail, existing ingredients, etc.)  
* `/health` and `/version` public endpoints  
* Docker Compose: one command brings up API + PostgreSQL  
* Init & seed scripts for quick local testing

---

## 🏗 Tech Stack

* **Python 3.10** | **FastAPI 0.110** | **SQLAlchemy 2.x**  
* **PostgreSQL 16** (official Docker image)  
* **Poetry** for dependency management  
* **Docker & Docker Compose**

---

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


### 🛠️ Initialize the Database

To create the tables inside the PostgreSQL database:

```bash
docker-compose exec api python -m scripts.init_db
```

💡 Make sure the recipes table does not already exist, or it will be ignored if already created.




### 🌱 Seed the Database

To insert initial data into the database for testing:

```bash
docker-compose exec api python -m scripts.seed_data
```


### 🔧 Environment Variables


| Variable       | Purpose                            | Default                                          |
| -------------- | ---------------------------------- | ------------------------------------------------ |
| `DATABASE_URL` | PostgreSQL connection              | `postgresql://postgres:postgres@db:5432/recipes` |


### 🛑 Stop the Containers

To stop and remove all containers, networks, and volumes:

```bash
# Stop the containers
docker-compose down
```


