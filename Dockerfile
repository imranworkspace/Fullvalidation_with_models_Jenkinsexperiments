# ---------- Base Image ----------
FROM python:3.9-slim

# ---------- Environment Variables ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- Working Directory ----------
WORKDIR /app

# ---------- System Dependencies ----------
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# ---------- Install Python Dependencies ----------
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# ---------- Copy Source Code ----------
COPY . /app/

# Copy .env into container
COPY .env /app/.env

# ---------- Collect Static Files (optional) ----------
RUN python manage.py collectstatic --noinput || true

# ---------- Default Command (for Django) ----------
CMD ["gunicorn", "formvalidation_with__model.wsgi:application", "--bind", "0.0.0.0:8011"]
