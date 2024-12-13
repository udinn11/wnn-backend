FROM python:3.9-slim

# environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 8080
EXPOSE 8080

# command for run app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
