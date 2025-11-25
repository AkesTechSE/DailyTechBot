# Use official slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables to prevent Python buffering issues
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create logs folder
RUN mkdir -p logs

# Create placeholder .env (will be overridden at runtime)
RUN touch .env

# Default command to run the bot
CMD ["python", "main.py"]
