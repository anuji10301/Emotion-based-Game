# Use official Python slim image
FROM python:3.12-slim

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

# Set the default command to run your app
CMD ["python", "app.py"]
