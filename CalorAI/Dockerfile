# Use Python slim image
FROM python:3.10-slim

# Set environment variables to reduce warnings and errors during builds
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies, including git
RUN apt-get update || (sleep 5 && apt-get update) || (sleep 10 && apt-get update) && \
    apt-get install -y --no-install-recommends \
    libpq-dev gcc git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=120 -r requirements.txt

# Copy project files
COPY . .

# Collect static files for Django
RUN python manage.py collectstatic --noinput

# Specify the default command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
