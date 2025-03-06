# File: backend/gemini_service/Dockerfile

FROM python:3.12-slim

WORKDIR /app

# ✅ Copy only required files, no `.env`
COPY ../requirements.txt /app/requirements.txt

# ✅ Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# ✅ Copy the gemini_service code
COPY gemini_service /app/gemini_service

# ✅ Expose port for service
EXPOSE 5000

# ✅ Use proper startup command
CMD ["uvicorn", "gemini_service.geminiRun:app", "--host", "0.0.0.0", "--port", "5000"]
