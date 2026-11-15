# Multi-stage or slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_CONFIG=production \
    PORT=5000

# Set working directory
WORKDIR /app

# Install system dependencies (curl for healthcheck, build-essential if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create instance directory for SQLite and set permissions
RUN mkdir -p instance && \
    chmod 777 instance

# Health check to ensure the application is responsive
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# Expose production port
EXPOSE 5000

# Entrypoint initializes the DB and runs Gunicorn WSGI server
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "--access-logfile=-", "--error-logfile=-", "run:app"]
