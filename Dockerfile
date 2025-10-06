# Use official Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libglib2.0-0 libsm6 libxrender1 libxext6 \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose the port (optional — Railway handles this)
EXPOSE 8000

# Start the app correctly using env PORT
CMD gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} app:app
