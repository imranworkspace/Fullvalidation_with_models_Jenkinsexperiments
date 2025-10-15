#!/bin/sh
# wait-for-db.sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 2
done
echo "PostgreSQL is up!"
