pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\imran\\AppData\\Local\\Programs\\Python\\Python38\\python.exe"
        DOCKER_IMAGE = "imrandocker24/formvalidation_with__model_jenkinsexperiments"
    }
    // for setcon job and take the backup into respective folder each 30 mins
    pipeline {
        agent any
        triggers {
            cron('H/30 * * * *')  // Every 30 minutes
        }

        environment {
            DB_NAME = "fpractice_db2"
            DB_USER = "postgres"
            BACKUP_DIR = "D:/jenkins_backups"
        }

        stages {
            stage('Backup Database') {
                steps {
                    script {
                        sh '''
                        echo "Cleaning old backups..."
                        find ${BACKUP_DIR} -name "*.sql" -mtime +1 -delete

                        echo "Creating new PostgreSQL backup..."
                        mkdir -p ${BACKUP_DIR}
                        docker exec -t db pg_dump -U ${DB_USER} ${DB_NAME} > ${BACKUP_DIR}/${DB_NAME}_$(date +%Y%m%d_%H%M%S).sql

                        echo "Backup completed successfully!"
                        '''
                    }
                }
            }
        }

        post {
            success {
                archiveArtifacts artifacts: '**/*.sql', fingerprint: true
            }
        }
    }
    // working code without cronjob and backup
    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/imranworkspace/Fullvalidation_with_models_Jenkinsexperiments'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    """
                }
            }
        }

        stage('Build & Run Containers') {
            steps {
                // Rebuild everything fresh
                bat 'docker-compose -f docker-compose.yml down || exit 0'
                bat 'docker-compose -f docker-compose.yml up -d --build'
            }
        }

        stage('Check Running Containers') {
            steps {
                bat 'docker ps -a'
            }
        }

        stage('Run Migrations & Collectstatic') {
            steps {
                // Wait for DB, then apply migrations & collect static files
                bat 'docker exec formvalidation_with__model_jenkinsexperiments python manage.py migrate --noinput'
                bat 'docker exec formvalidation_with__model_jenkinsexperiments python manage.py collectstatic --noinput'
            }
        }

        // stage('Push Docker Image') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
        //             bat """
        //                 echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
        //                 docker build -t %DOCKER_IMAGE% .
        //                 docker push %DOCKER_IMAGE%
        //             """
        //         }
        //     }
        // }
    }
}
