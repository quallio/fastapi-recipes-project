# Use official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy Poetry config files first to leverage Docker layer cache
COPY pyproject.toml poetry.lock* /app/

# Install Poetry and configure it to install dependencies in the global environment (global since it is happening in the container)
RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Copy the entire project into the container
COPY . /app/

# Expose the FastAPI default port
EXPOSE 8000

# Default command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
