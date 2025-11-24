FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py .

# Create .env file placeholder (should be mounted at runtime)
RUN touch .env

# Run the bot
CMD ["python", "main.py"]
