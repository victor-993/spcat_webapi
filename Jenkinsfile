pipeline {

    agent any

    stages {
        stage('Ssh') {
            steps {
                script {
                    withCredentials(bindings: [sshUserPrivateKey(credentialsId: 'KEY_SPCAT', keyFileVariable: 'SSH_KEY')]) {
                        def remote = [name: "Parks", host: "172.30.1.114", user: "spcat", allowAnyHosts: true, identityFile: SSH_KEY]
                        sshCommand remote: remote, sudo: false, command: "ls"
                    }
                }
            }
        }
        stage('Get release') {
            steps {
                sh """ls"""
                //sh """ls"""
                //sh """rm -fr src"""
                //sh """rm -fr releaseApi.zip"""
            }
        }
    }
 
}

/* pipeline {
    agent any

    environment {
        remote = null
    }
    
    stages {
        stage('SSH to AWS server') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'KEY_SPCAT', keyFileVariable: 'SSH_KEY')]) {
                        def remote = [:]
                        remote.name = credentials('Parks')
                        remote.host = credentials('172.30.1.114')
                        remote.user = credentials('spcat')
                        remote.allowAnyHosts = true
                        remote.identityFile = SSH_KEY

                        // Definir la variable remote fuera del bloque script
                        env.remote = remote

                        
                        sshCommand remote: remote, sudo: false, command: '''
                            # Inicio de sesión en el servidor AWS
                            # Verificar y crear la carpeta api_SPCAT si no existe y el entorno virtual
                            if [ -d api_SPCAT ]; then
                                cd ./api_SPCAT
                            else
                                mkdir ./api_SPCAT
                                cd ./api_SPCAT
                                python3 -m venv env
                            fi
                        '''
                    }
                }
            }
        }
        
        stage('Stop previous API') {
            steps {
                script {
                    sshCommand remote: env.remote, command: '''
                        # Detener la API si está en ejecución
                        if [ -n "$PID_API_SPCAT" ]; then
                            kill "$PID_API_SPCAT"
                        fi
                    '''
                }
            }
        }
        
        stage('Backup previous files') {
            steps {
                script {
                    sshCommand remote: env.remote, command: '''
                        # Guardar archivos antiguos de la API
                        rm -rf api_antiguo
                        mv api_actual api_antiguo
                    '''
                }
            }
        }
        
        stage('Download latest release') {
            steps {
                script {
                    sshCommand remote: env.remote, command: '''
                        # Descargar el último release desde GitHub
                        rm -rf releaseApi.zip
                        curl -LOk https://github.com/victor-993/spcat_webapi/releases/latest/download/releaseApi.zip
                        rm -rf api_actual
                        unzip releaseApi.zip -d api_actual
                    '''
                }
            }
        }
        
        stage('Update dependencies') {
            steps {
                script {
                    sshCommand remote: env.remote, command: '''
                        # Acceder al entorno virtual
                        source env/bin/activate
                        
                        # Actualizar las dependencias
                        pip install -r api_actual/requirements.txt
                    '''
                }
            }
        }
        
        stage('Start API') {
            steps {
                script {
                    sshCommand remote: env.remote, command: '''
                        # Iniciar la API
                        nohup python3 api_actual/api.py > log.txt 2>&1 &
                        
                        # Obtener el nuevo PID y guardarlo en un archivo
                        PID_API_SPCAT=$!
                        echo $PID_API_SPCAT > pid.txt
                    '''
                }
            }
        }
    }

    post {
        success {
            emailext(
                subject: "Successful deployment of the SPCAT API",
                body: "The SPCAT api pipeline has been executed correctly.",
                recipientProviders: [developers()],
                replyTo: "vhernandez@cgiar.org"
            )
        }
        failure {
            emailext(
                subject: "Failure to deploy the SPCAT API",
                body: "The SPCAT api pipeline has failed at step ${currentBuild.currentResult.displayName}. Por favor, revisa los registros de Jenkins para obtener más detalles.",
                recipientProviders: [developers()],
                replyTo: "vhernandez@cgiar.org"
            )
        }
    }
} */