# Base image
FROM python:3.10-bullseye

# Environment variables to improve runtime behavior
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /school_managment_saas

# Copy application code to the container
ADD . /school_managment_saas/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-client \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8001

# CMD to start the application
CMD ["gunicorn", "school_managment_saas.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "3", "--threads", "2", "--timeout", "500"]
