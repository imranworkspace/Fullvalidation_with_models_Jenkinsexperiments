pipeline {
    agent any

    // ---------------- Environment Variables ----------------
    stages {
        stage('Load Environment Variables') {
            steps {
                script {
                    // Read the .env file into a Map
                    def envVars = readProperties file: '.env'

                    // Assign values to Jenkins global environment
                    env.PYTHONPATH = envVars.PYTHONPATH
                    env.DOCKER_IMAGE = envVars.DOCKER_IMAGE
                    env.POSTGRES_DB = envVars.POSTGRES_DB
                    env.POSTGRES_PASSWORD = envVars.POSTGRES_PASSWORD
                    env.DB_BKP_PATH = envVars.DB_BKP_PATH

                    // Aliases for convenience
                    env.PYTHON = env.PYTHONPATH
                    env.BACKUP_DIR = env.DB_BKP_PATH
                }

                echo "✅ Loaded environment variables from .env"
                echo "Docker Image: ${env.DOCKER_IMAGE}"
                echo "Backup Dir: ${env.BACKUP_DIR}"
            }
        }
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
        // health chk
        // stage('Health Check') {
        //     steps {
        //         script {
        //             bat 'curl -f http://localhost:81/reg/ || exit 1'
        //         }
        //     }
        // }

    }

    // ---------------- Post Actions [TAKING SQL BACKUP & SENDING EMAIL STATUS OF BUILD]----------------
    
    post {
        success {
                    archiveArtifacts artifacts: 'D:/jenkins_backups/*.sql', fingerprint: true, allowEmptyArchive: true
                    //
                    echo "${env.BUILD_NUMBER}"
                    echo "${env.JOB_NAME}"
                    echo "${env.BUILD_URL}"
                    echo "${BACKUP_DIR}"

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
                            to: "shaikh.novetrics@gmail.com",
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
                        to: "shaikh.novetrics@gmail.com",
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
