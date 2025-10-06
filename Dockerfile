# Use official Python slim image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install build tools required to compile some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files
COPY . .

# Expose port 8000 for Flask app
EXPOSE 8000

# Run the Flask app
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} app:app"]


