/* pipeline {

    agent any

    stages {
        stage('Ssh') {
            steps {
                script {
                    withCredentials(bindings: [sshUserPrivateKey(credentialsId: '', keyFileVariable: 'SSH_KEY')]) {
                        def remote = [name: "Parks", host: "", user: "", allowAnyHosts: true, identityFile: SSH_KEY]
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
 
} */

def remote = [:]
pipeline {
    agent any

    environment {
        server = credentials('name_fertilizer')
        algo = credentials('host_fertilizer')
        SSH_CREDS = credentials('fertalizer_devops')
    }

    stages {
        stage('SSH to AWS server') {
            steps {
                script {
                    
                    remote.allowAnyHosts = true
                    remote.identityFile = SSH_CREDS
                    remote.user = SSH_CREDS_USR
                    remote.name = server
                    remote.host = algo

                    sshCommand remote: remote, command: "ls"
                    
                    /* sshCommand remote: remote, command: '''
                        # Inicio de sesión en el servidor AWS
                        # Verificar y crear la carpeta api_SPCAT si no existe y el entorno virtual
                        if [ -d api_SPCAT ]; then
                            cd ./api_SPCAT
                        else
                            mkdir ./api_SPCAT
                            cd ./api_SPCAT
                            python3 -m venv env
                        fi
                    ''' */
                    
                }
            }
        }

        stage('segundo') {
            steps {
                script {

                    echo "remote: ${remote}"
                    sh 'printenv'
                }
            }
        }
        
        /* stage('Stop previous API') {
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
        } */
    }
}