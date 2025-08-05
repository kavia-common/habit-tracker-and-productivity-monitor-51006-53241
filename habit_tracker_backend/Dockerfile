# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the FastAPI port
EXPOSE 3001

# Default command to run FastAPI with uvicorn on 0.0.0.0:3001
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "3001", "--reload"]
