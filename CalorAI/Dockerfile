# Use Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=120 -r requirements.txt

# Copy project files
COPY . .

# Run collectstatic (if needed)
RUN python manage.py collectstatic --noinput
