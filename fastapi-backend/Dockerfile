# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]