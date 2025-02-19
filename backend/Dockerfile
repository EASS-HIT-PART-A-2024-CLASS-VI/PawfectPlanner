# Use the latest supported Python version
FROM python:3.12-slim  

# Set the working directory inside the container
WORKDIR /app  

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip  

# Copy the requirements file first to cache dependencies efficiently
COPY ./requirements.txt .  

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the entire backend application
COPY . .  

# Expose FastAPI default port
EXPOSE 8000  

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
