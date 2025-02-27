# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install dependencies, ensuring `uvicorn` and `python-multipart` are included
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir uvicorn python-multipart

# Copy the entire backend code
COPY . /app

# Expose the application port
EXPOSE 8000

# Ensure Uvicorn runs properly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]