# Base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# ✅ Fix the COPY command if `gemini-service` is inside `backend/`
COPY ./requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Fix the COPY command for the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Add a healthcheck (optional)
HEALTHCHECK CMD curl --fail http://localhost:5000/healthcheck || exit 1

# Start the application
CMD ["uvicorn", "gemini_service:app", "--host", "0.0.0.0", "--port", "5000"]
