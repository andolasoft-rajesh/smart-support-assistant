# backend/Dockerfile
# Packages the FastAPI app so `docker compose up` needs no local Python.
FROM python:3.12-slim

WORKDIR /app

# Install deps first so the layer caches when only app code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code. (.dockerignore keeps venv/__pycache__/.env out of the image.)
COPY . .

EXPOSE 8000

# 0.0.0.0 so the port is reachable from outside the container, not just
# localhost inside it. One worker is plenty for a demo stack.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
