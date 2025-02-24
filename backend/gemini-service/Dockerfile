# Use the same Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the Gemini service files
COPY . .

# Command to run the service
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
