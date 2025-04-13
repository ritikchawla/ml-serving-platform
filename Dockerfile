# Use a slim Python base image
FROM python:3.11-slim

# Create a non-root user
RUN groupadd -r mlserver && useradd -r -g mlserver mlserver

# Set working directory
WORKDIR /app

# Install system dependencies with fixed versions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential=12.9 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .
RUN chown mlserver:mlserver requirements.txt && \
    chmod 644 requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
RUN chown -R mlserver:mlserver src/ && \
    chmod -R 644 src/ && \
    find src/ -type d -exec chmod 755 {} \;

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER mlserver

# Create necessary directories with correct permissions
RUN mkdir -p /app/models /app/tmp && \
    chmod 755 /app/models /app/tmp

# Expose ports for HTTP and metrics
EXPOSE 8080 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["uvicorn", "src.model_server.server:app", "--host", "0.0.0.0", "--port", "8080"]