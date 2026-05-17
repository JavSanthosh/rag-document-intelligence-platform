# Dockerfile
# This file tells Docker how to package your app into a container
# Think of it like a recipe: "start with Python, install these, run this"

# Start with official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (Docker caches this layer - faster rebuilds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into container
COPY . .

# Create folder for ChromaDB to store data
RUN mkdir -p /app/chroma_db

# Expose port 8000 (FastAPI runs here)
EXPOSE 8000

# Command to start the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]