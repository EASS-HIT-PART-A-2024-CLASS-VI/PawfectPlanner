# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Add the app directory to PYTHONPATH
ENV PYTHONPATH=/app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY . /app

# Expose the microservice port
EXPOSE 5000

# Command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
