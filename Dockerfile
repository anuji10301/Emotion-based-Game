# Use full Python image to avoid missing system libs
FROM python:3.12

WORKDIR /app

# Install system dependencies for common scientific libs
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (Railway uses $PORT)
EXPOSE 8000

# Start command
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} app:app"]
