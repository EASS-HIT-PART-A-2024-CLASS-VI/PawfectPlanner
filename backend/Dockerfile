# File: backend/Dockerfile

FROM python:3.12-slim

WORKDIR /app

# 1) Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 2) Make /app the package root
ENV PYTHONPATH=/app

# 3) Copy all backend code into /app
COPY . /app

# 4) Expose port 8000 for the API
EXPOSE 8000

# 5) Run the FastAPI app using uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
