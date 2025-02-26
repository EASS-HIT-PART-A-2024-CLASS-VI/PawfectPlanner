# Use the same Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the application code (no need to copy requirements.txt)
COPY gemini-service/ .  

# Expose the application port
EXPOSE 5000

# Run the service
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
