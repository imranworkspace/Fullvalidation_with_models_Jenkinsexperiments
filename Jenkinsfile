pipeline {
    agent any

    // ---------------- Environment Variables ----------------
    environment {
        PYTHON = "C:\\Users\\imran\\AppData\\Local\\Programs\\Python\\Python38\\python.exe"
        DOCKER_IMAGE = "imran3656/formvalidation_with_jenkinsexperiments"
        DB_NAME = "fpractice_db2"
        DB_USER = "postgres"
        BACKUP_DIR = "D:/jenkins_backups"
    }

    // ---------------- CRON Schedule ----------------
    triggers {
        cron('H/30 * * * *')  // every 30 mins
    }

    stages {

        // 1️⃣ Checkout Code
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/imranworkspace/Fullvalidation_with_models_Jenkinsexperiments'
            }
        }

        // 2️⃣ Docker Login
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    """
                }
            }
        }

        // 3️⃣ Build & Push Docker Image
        stage('Build & Push Docker Image') {
            steps {
                bat """
                    docker build -t ${DOCKER_IMAGE}:latest .
                    docker push ${DOCKER_IMAGE}:latest
                """
            }
        }

        // 4️⃣ Run Containers using docker-compose
        stage('Run Containers') {
            steps {
                bat 'docker-compose -f docker-compose.yml down || exit 0'
                bat 'docker-compose -f docker-compose.yml up -d'
            }
        }

        // 5️⃣ Check Running Containers
        stage('Check Running Containers') {
            steps {
                bat 'docker ps -a'
            }
        }

        // 6️⃣ Run Migrations & Collectstatic
        stage('Run Migrations & Collectstatic') {
            steps {
                bat 'docker exec formvalidation_with__model_jenkinsexperiments python manage.py migrate --noinput'
                bat 'docker exec formvalidation_with__model_jenkinsexperiments python manage.py collectstatic --noinput'
            }
        }

        // 7️⃣ Health Check
        stage('Health Check') {
            steps {
                script {
                    bat 'curl -f http://localhost:81/reg/ || exit 1'
                }
            }
        }

        // 8️⃣ Backup Database
        stage('Backup Database') {
            steps {
                script {
                    bat """
                        echo Cleaning old backups...
                        forfiles /p "${BACKUP_DIR}" /m *.sql /d -1 /c "cmd /c del @path"

                        echo Creating new PostgreSQL backup...
                        if not exist "${BACKUP_DIR}" mkdir "${BACKUP_DIR}"
                        docker exec -t db_jenkinsexp pg_dump -U ${DB_USER} ${DB_NAME} > "${BACKUP_DIR}\\${DB_NAME}_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.sql"
                        
                        echo Backup completed successfully!
                    """
                }
            }
        }

        // ---------------- Backup Stage ----------------
        stage('Backup Database') {
            steps {
                script {
                    bat """
                        echo Cleaning old backups...
                        forfiles /p "${BACKUP_DIR}" /m *.sql /d -1 /c "cmd /c del @path"

                        echo Creating new PostgreSQL backup...
                        if not exist "${BACKUP_DIR}" mkdir "${BACKUP_DIR}"
                        docker exec -t fullvaliation_jenkinsexperiments-db_jenkinsexp-1 pg_dump -U ${DB_USER} ${DB_NAME} > "${BACKUP_DIR}\\${DB_NAME}_%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.sql"
                        
                        echo Backup completed successfully!
                    """
                }
            }
        }

    }

}