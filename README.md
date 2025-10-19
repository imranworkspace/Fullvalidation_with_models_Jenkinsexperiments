# 🚀 Django Form Validation with Jenkins, Docker, Redis, Celery, PostgreSQL, and Nginx

This project demonstrates a **CI/CD pipeline** setup using **Jenkins**, **Docker**, **Docker Compose**, and **AWS**, deploying a **Django web application** integrated with **Redis**, **Celery**, **PostgreSQL**, and **Nginx**.  
It includes automated builds, migrations, static file collection, and email notifications for build results.

---

## 🧩 Project Overview

| Component | Description |
|------------|-------------|
| **Framework** | Django |
| **CI/CD Tool** | Jenkins |
| **Containerization** | Docker & Docker Compose |
| **Database** | PostgreSQL |
| **Cache & Broker** | Redis |
| **Task Queue** | Celery + Celery Beat |
| **Monitoring Tool** | Flower |
| **Web Server** | Nginx |
| **Backup & Notifications** | Jenkins Post-Build SQL backup and email alerts |

---

## 📁 Project Structure

```
.
├── Jenkinsfile
├── docker-compose.yml
├── Dockerfile
├── .env
├── nginx/
│   └── nginx.conf
├── formvalidation_with__model/
│   ├── views.py
│   ├── models.py
│   ├── studentform.py
│   ├── templates/
│   │   ├── reg.html
│   │   ├── login.html
│   │   ├── home.html
│   │   └── logout.html
└── requirements.txt
```

---

## 🧱 Jenkinsfile

This is the **pipeline configuration** used by Jenkins for CI/CD automation.

### 🔹 Features
- **Git Checkout**: Clones the main branch from GitHub.
- **Docker Login**: Authenticates using Jenkins credentials (`dockerhub-creds`).
- **Container Build/Run**: Builds Docker images and runs containers using `docker-compose`.
- **Migrations & Static Files**: Executes Django management commands.
- **Post Actions**:
  - Creates PostgreSQL backups.
  - Sends **email notifications** for success/failure using Gmail credentials (`786gmail`).
- **Automated Cron Trigger**: Runs every 30 minutes.

### ⚙️ Pipeline Flow
```groovy
Checkout Code → Docker Login → Build & Run → Run Migrations → Send Email (Success/Failure)
```

---

## 🐳 docker-compose.yml

Defines and orchestrates multiple services required for the Django application.

| Service | Description |
|----------|-------------|
| **django_jenkinsexp** | Django web app (port 8011) |
| **redis** | Caching and Celery message broker (port 6380) |
| **celery** | Celery worker processing background tasks |
| **celery-beat** | Schedules periodic Celery tasks |
| **flower** | Celery monitoring dashboard (port 5556) |
| **db_jenkinsexp** | PostgreSQL database |
| **nginx** | Reverse proxy and static file server (port 81) |

### 🧠 Volumes
- `postgres_data`: Persists PostgreSQL data.
- `.:/app`: Maps local Django source into the container.

---

## 🐍 Dockerfile

Defines how the Django app image is built.

### 🔹 Steps
1. Uses `python:3.9-slim` base image.
2. Installs dependencies (`build-essential`, `libpq-dev`).
3. Installs Python packages from `requirements.txt`.
4. Copies source code and `.env` into `/app`.
5. Collects static files.
6. Runs the app via **Gunicorn** on port **8011**.

### 🔧 Default Command
```bash
CMD ["gunicorn", "formvalidation_with__model.wsgi:application", "--bind", "0.0.0.0:8011"]
```

---

## ⚙️ .env File

Environment configuration shared across Django, PostgreSQL, Redis, and Jenkins.

### 🧾 Example Content
```bash
# Django
DJANGO_SECRET_KEY='django-insecure-toww60*fwetc^ri)b$brb-9zrgg-)j-t+hjiyf__08k2y0yi%2'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=fpractice_db2
POSTGRES_USER=postgres
POSTGRES_PASSWORD=imrandell
DB_HOST=db_jenkinsexp
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=2

# Celery
CELERY_BROKER_URL=redis://redis:6379/2
CELERY_RESULT_BACKEND=redis://redis:6379/2

# Nginx
NGINX_PORT=81

# Git
GIT_BRANCH=main
GIT_REPO=https://github.com/imranworkspace/Fullvalidation_with_models_Jenkinsexperiments
```

---

## 🌐 nginx.conf

Handles reverse proxying and static/media file serving.

### 🔹 Configuration Highlights
```nginx
server {
    listen 81;
    server_name localhost;

    location / {
        proxy_pass http://django_jenkinsexp:8011;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /formvalidation_with__model/static/;
    }

    location /media/ {
        alias /formvalidation_with__model/media/;
    }
}
```

---

## 🧠 views.py (Django App)

Implements form-based registration and login with Celery task integration.

### 🔹 Key Functions
| Function | Description |
|-----------|-------------|
| `registrationForm()` | Handles user registration form and background Celery tasks (`mul`, `visit_cache`). |
| `homepage()` | Displays session info and user data after login. |
| `login()` | Authenticates users using `StudentModel`. |
| `logout()` | Clears user session and redirects to logout page. |

### 🔹 Celery Tasks
- `mul.delay(1,5)` – performs background multiplication.
- `visit_cache.delay()` – updates visit count in Redis cache.

---

## 🛠️ Jenkins Credentials Required

| ID | Type | Usage |
|----|------|--------|
| `dockerhub-creds` | Username/Password | Docker Hub login |
| `786gmail` | Username/Password | Email notifications (Gmail) |
| `deploy-key` *(optional)* | SSH Key | Deployment to remote server |

---

## 🧾 Automated SQL Backup (Post-Build)

Backups are created after a successful pipeline run and archived to:
```
D:/jenkins_backups/
```

---

## 📬 Email Notification Examples

### ✅ Success Email
Subject: `SUCCESS: Django Jenkins Pipeline Completed`  
Body: Includes build number, job name, and backup path.

### ❌ Failure Email
Subject: `FAILED: Django Jenkins Pipeline Error`  
Body: Contains failure notice and build URL.

---

## 🚀 How to Run Locally

```bash
# 1️⃣ Build containers
docker-compose up -d --build

# 2️⃣ Run migrations & collect static
docker exec formvalidation_with__model_jenkinsexperiments python manage.py migrate --noinput
docker exec formvalidation_with__model_jenkinsexperiments python manage.py collectstatic --noinput

# 3️⃣ Access application
http://localhost:81/reg/  → Registration Page  
http://localhost:81/login/ → Login Page  
http://localhost:5556/     → Celery Flower Dashboard
```

---

## 🧰 Tech Stack Summary

- **Backend**: Django (Python)
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL
- **Frontend**: HTML Templates (Bootstrap)
- **DevOps**: Jenkins, Docker, Docker Compose, Nginx
- **Deployment**: AWS EC2 (recommended)

---

## 👨‍💻 Author

**Imran Shaikh**  
📧 [shaikh.novetrics@gmail.com](mailto:shaikh.novetrics@gmail.com)  
🔗 [GitHub – imranworkspace](https://github.com/imranworkspace)
