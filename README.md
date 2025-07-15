# 🍲 FastAPI Recipes App (Backend + Frontend)

Production-ready fullstack app to manage **recipes**, **ingredients**, and **authors**, built with:

- 🐍 **FastAPI** backend + **PostgreSQL**
- ⚛️ **React** frontend + Vite
- 🐳 **Docker Compose** for orchestration

---

## ✨ Features

### ✅ Backend

| Layer            | Responsibility                      | Folder           |
|------------------|--------------------------------------|------------------|
| Presentation     | HTTP routes & Pydantic DTOs         | `app/presentation` |
| Application      | Business logic & validation rules   | `app/application`  |
| Domain           | SQLAlchemy ORM models               | `app/domain`       |
| Persistence      | DB access / repositories            | `app/persistence`  |

- Full CRUD: Authors, Recipes, Ingredients
- Validation: unique emails, ingredient existence, etc.
- Data transformation: returns nested authors and ingredient names
- Swagger docs at `/docs`
- Health check at `/health`
- Includes DB init and seed scripts

### 🌐 Frontend (React)

- Built with React 18 + Vite 5
- Allows viewing and creating recipes
- Recipe form supports multiple ingredients
- Form-level validation
- Basic mobile responsiveness
- **Note**: API URL is currently hardcoded to `http://localhost:8000`  
  (see `frontend/src/api/recipeApi.js`)

---

## 📦 Tech Stack

- **Python 3.10**, FastAPI 0.110, SQLAlchemy 2.x
- PostgreSQL 16 (Dockerized)
- React, Vite, Axios
- Poetry for dependency management
- Docker + Docker Compose

---

## 🐳 Prerequisites

Before starting, ensure you have the following installed:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🚀 Getting Started

You can run the entire app (backend + frontend + db) using:

```bash
docker-compose up --build
```

This will start:

| Service     | URL                            |
|-------------|---------------------------------|
| **Backend** | http://localhost:8000           |
| **Frontend**| http://localhost:5173           |
| **Docs**    | http://localhost:8000/docs      |
| **Database**| PostgreSQL on `localhost:5432`  |

---


## 🧪 Running Tests

### To run the unit tests inside the Docker container:

```bash
docker-compose run --rm api pytest -v -s
```

This command will:

- Create a temporary container based on the api service
- Run all tests using pytest
- Show detailed output (-v) and any print() statements (-s)
- Automatically remove the container after completion (--rm)


## 🛠 Database Setup

### Initialize tables

```bash
docker-compose exec api python -m scripts.init_db
```

### Seed sample data

```bash
docker-compose exec api python -m scripts.seed_data
```

---

## 📁 Project Structure

```
.
├── app/                 # FastAPI backend (clean architecture)
│   ├─ presentation/     # HTTP routes & Pydantic DTOs
│   ├─ application/      # Business services & domain rules
│   ├─ domain/           # ORM entities
│   └─ persistence/      # Repositories / DB access
├── frontend/            # React frontend (Vite)
├── scripts/             # DB init & seed
├── docs/                # Architecture diagrams (Mermaid .mmd files)
├── docker-compose.yml   # Orchestration
└── README.md
```

Inside `frontend/`:

```
src/
 ├─ api/
 │   └─ recipeApi.js         # Axios wrappers
 ├─ components/
 │   ├─ RecipeList/
 │   │   └─ RecipeList.jsx
 │   └─ RecipeForm/
 │       ├─ RecipeForm.jsx
 │       └─ IngredientField.jsx
 ├─ App.jsx
 ├─ main.jsx
 └─ index.css
```

---

## 🔁 Business Transformation

The backend returns each recipe in a denormalized format that includes:

- Author info
- Ingredient name + quantity + unit

Example:

```json
{
  "id": 1,
  "title": "Pancakes",
  "description": "...",
  "author": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com"
  },
  "ingredients": [
    { "ingredient_id": 2, "ingredient_name": "Flour", "quantity": 200, "unit": "g" },
    { "ingredient_id": 3, "ingredient_name": "Milk",  "quantity": 250, "unit": "ml" }
  ]
}
```

This lets the frontend render recipes **without extra API calls**.

---

## 🔧 Environment Notes

The API URL used by the frontend is currently hardcoded to `http://localhost:8000`.  
Support for `.env` will be added in a future update.

---

## ✅ Future Improvements

- `.env` support for frontend API base URL
- Edit/Delete support for recipes
- Recipe images or categories
- Pagination / filtering in the frontend
- Improved validation UX (Yup/Zod)
- **Unit tests** (Pytest) & **integration tests**
- Pre‑commit quality tools (e.g. **Flake8**, Black)

---

### 🧹 Pre-commit Hooks

Pre-commit hooks are configured to maintain code quality and consistency across the project.

They include:

- **Ruff** — formatting and linting (`--fix`)
- **Mypy** — static type checking
- **Pylint** — linting with a minimum score threshold

Once installed, they run automatically on every `git commit`.  
You can also run them manually on all files with:

```bash
poetry run pre-commit run --all-files
```

> ℹ️ Make sure you’ve installed pre-commit with:
>
> ```bash
> poetry add --dev pre-commit
> poetry run pre-commit install
> ```



> ### Personal Note 
> Building this project was a great learning exercise; it kept me busy and exposed me to new concepts.  
> In hindsight I should have leveraged Git branches and pull‑request workflows even when working solo, keeping `main` always deployable and merging feature branches incrementally — a practice I do follow in professional settings.

## 📝 License

MIT



