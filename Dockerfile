# Use a small Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies (optional, but good practice)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose the port the app will run on
EXPOSE 5000

# Use gunicorn to run the app in production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
