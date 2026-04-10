# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY api_project.py .

# Expose Flask default port
EXPOSE 5000

# Run the Flask application
CMD ["python", "api_project.py"]

