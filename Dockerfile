# Dockerfile

# Start with official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (Docker caches this layer)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create ChromaDB storage directory
RUN mkdir -p /app/chroma_db

# FastAPI runs on port 8000
EXPOSE 8000

# Show logs immediately in Docker
ENV PYTHONUNBUFFERED=1

# Start FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
