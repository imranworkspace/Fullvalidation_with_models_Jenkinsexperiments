#!/bin/sh
set -e

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username="test").exists():
    User.objects.create_superuser("test", "test@example.com", "imran123")
    print("Superuser 'test' created")
else:
    print("Superuser 'test' already exists")
EOF

echo "Starting server..."
python manage.py runserver 0.0.0.0:8010
