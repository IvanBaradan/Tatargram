# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Copy application code
COPY . .

# Set PYTHONPATH to include the current directory
ENV PYTHONPATH=/app

# Create session file with proper permissions
RUN touch /app/telegram_session.session && \
    chown app:app /app/telegram_session.session && \
    chmod 666 /app/telegram_session.session

# Switch to app user
USER app

# Expose port
EXPOSE 8001

# Command to run the application
CMD ["python", "telegram_api/main.py"]