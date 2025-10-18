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
        cron('H/30 * * * *') // Run every 30 minutes
    }

    // ---------------- Pipeline Stages ----------------
    stages {

        stage('Load Environment Variables') {
            steps {
                script {
                    // Read the .env file into a Map
                    def envVars = readProperties file: '.env'

                    // Assign values to Jenkins environment
                    env.PYTHONPATH = envVars.PYTHONPATH
                    env.DOCKER_IMAGE = envVars.DOCKER_IMAGE
                    env.POSTGRES_DB = envVars.POSTGRES_DB
                    env.POSTGRES_PASSWORD = envVars.POSTGRES_PASSWORD
                    env.DB_BKP_PATH = envVars.DB_BKP_PATH

                    // Aliases
                    env.PYTHON = env.PYTHONPATH
                    env.BACKUP_DIR = env.DB_BKP_PATH

                }

                echo "✅ Loaded environment variables from .env"
                echo "Docker Image: ${env.DOCKER_IMAGE}"
                echo "Backup Dir: ${env.BACKUP_DIR}"
            }
        }

        stage('Checkout Code') {
            steps {
                script {
                    // Load .env file
                    def envVars = readProperties file: '.env'

                    // Export variables
                    env.GIT_BRANCH = envVars.GIT_BRANCH
                    env.GIT_REPO = envVars.GIT_REPO

                    echo "Checking out branch: ${env.GIT_BRANCH}"
                    echo "Repository: ${env.GIT_REPO}"

                    // Use the environment variables
                    git branch: env.GIT_BRANCH, url: env.GIT_REPO
                }
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

        // Optional Health Check
        // stage('Health Check') {
        //     steps {
        //         bat 'curl -f http://localhost:81/reg/ || exit 1'
        //     }
        // }

    }

    // ---------------- Post Actions ----------------
    post {
        success {
            archiveArtifacts artifacts: 'D:/jenkins_backups/*.sql', fingerprint: true, allowEmptyArchive: true

            echo "Build Number: ${env.BUILD_NUMBER}"
            echo "Job Name: ${env.JOB_NAME}"
            echo "Build URL: ${env.BUILD_URL}"
            echo "Backup Dir: ${env.BACKUP_DIR}"

            withCredentials([usernamePassword(credentialsId: '786gmail', usernameVariable: 'MAIL_USER', passwordVariable: 'MAIL_PASS')]) {
                emailext(
                    subject: "✅ SUCCESS: Django Jenkins Pipeline Completed",
                    body: """<p>Hi Team,</p>
                             <p>The Jenkins pipeline for <b>Form Validation Django Project</b> completed successfully.</p>
                             <p>Backup has been created in: <b>${env.BACKUP_DIR}</b></p>
                             <p>Build Details:</p>
                             <ul>
                             <li>Build Number: ${env.BUILD_NUMBER}</li>
                             <li>Job: ${env.JOB_NAME}</li>
                             <li>URL: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></li>
                             </ul>
                             <p>– Jenkins</p>""",
                    to: "shaikh.novetrics@gmail.com",
                    from: "${MAIL_USER}",
                    replyTo: "${MAIL_USER}",
                    mimeType: 'text/html'
                )
            }
        }

        failure {
            echo '❌ Pipeline failed. Check the console output for errors.'

            withCredentials([usernamePassword(credentialsId: '786gmail', usernameVariable: 'MAIL_USER', passwordVariable: 'MAIL_PASS')]) {
                emailext(
                    subject: "❌ FAILED: Django Jenkins Pipeline Error",
                    body: """<p>Hi Team,</p>
                             <p>The Jenkins pipeline for <b>Form Validation Django Project</b> has failed.</p>
                             <p>Please check the console logs for more details:</p>
                             <p><a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                             <p>– Jenkins</p>""",
                    to: "shaikh.novetrics@gmail.com",
                    from: "${MAIL_USER}",
                    replyTo: "${MAIL_USER}",
                    mimeType: 'text/html'
                )
            }
        }
    }
}
