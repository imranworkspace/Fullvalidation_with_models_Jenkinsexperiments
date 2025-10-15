# Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

# Collect static files (optional, can run at container start)
RUN python manage.py collectstatic --noinput

# Run Gunicorn
CMD ["gunicorn", "formvalidation_with__model.wsgi:application", "--bind", "0.0.0.0:8010"]

