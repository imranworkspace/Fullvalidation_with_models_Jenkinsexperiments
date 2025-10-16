pipeline {
    agent any

    // ---------------- Environment Variables ----------------
    environment {
        PYTHON = "C:\\Users\\imran\\AppData\\Local\\Programs\\Python\\Python38\\python.exe"
        DOCKER_IMAGE = "imrandocker24/formvalidation_with__model_jenkinsexperiments"
        DB_NAME = "fpractice_db2"
        DB_USER = "postgres"
        BACKUP_DIR = "D:/jenkins_backups"
    }

    // ---------------- CRON Schedule ----------------
    // Run automatically every 30 minutes
    triggers {
        cron('H/30 * * * *')
    }

    // ---------------- Pipeline Stages ----------------
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
                bat 'docker exec formvalidation_with__model_jenkinsexperiments python manage.py migrate --noinput'
                bat 'docker exec formvalidation_with__model_jenkinsexperiments python manage.py collectstatic --noinput'
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

    // ---------------- Post Actions ----------------
    post {
        success {
                    archiveArtifacts artifacts: 'D:/jenkins_backups/*.sql', fingerprint: true, allowEmptyArchive: true
                    // Send success email using credentials
                    withCredentials([usernamePassword(credentialsId: '786gmail', usernameVariable: 'MAIL_USER', passwordVariable: 'MAIL_PASS')]) {
                        emailext (
                            subject: "✅ SUCCESS: Django Jenkins Pipeline Completed",
                            body: """<p>Hi Team,</p>
                                    <p>The Jenkins pipeline for <b>Form Validation Django Project</b> completed successfully.</p>
                                    <p>Backup has been created in: <b>${BACKUP_DIR}</b></p>
                                    <p>Build Details:</p>
                                    <ul>
                                    <li>Build Number: ${env.BUILD_NUMBER}</li>
                                    <li>Job: ${env.JOB_NAME}</li>
                                    <li>URL: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></li>
                                    </ul>
                                    <p>– Jenkins</p>""",
                            to: "imranlatur786@gmail.com",
                            from: "${MAIL_USER}",
                            replyTo: "${MAIL_USER}",
                            mimeType: 'text/html'
                        )
                    }
        }
        failure {
            echo 'Pipeline failed. Check the console output for errors.'
            failure {
            script {
                withCredentials([usernamePassword(credentialsId: '786gmail', usernameVariable: 'MAIL_USER', passwordVariable: 'MAIL_PASS')]) {
                    emailext (
                        subject: "❌ FAILED: Django Jenkins Pipeline Error",
                        body: """<p>Hi Team,</p>
                                 <p>The Jenkins pipeline for <b>Form Validation Django Project</b> has failed.</p>
                                 <p>Please check the console logs for more details:</p>
                                 <p><a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                 <p>– Jenkins</p>""",
                        to: "imranlatur786@gmail.com",
                        from: "${MAIL_USER}",
                        replyTo: "${MAIL_USER}",
                        mimeType: 'text/html'
                    )
                }
            }
        }
        }
    }
   
}
