# 1. Use a lightweight Python version
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements first (this makes rebuilding faster)
COPY requirements.txt .

# 4. Install the libraries Shaurya used for the API
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all the code from your local folder into the container
COPY . .

# 6. Tell Docker which port the API will use (Usually 8000 for FastAPI/Flask)
EXPOSE 8000

# 7. The command to start the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "run_api.py"]