// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {
    agent any

    environment {
        server_name = credentials('name_spcat')
        server_host = credentials('host_spcat')
        ssh_key = credentials('spcat_key')
        port_api = credentials('api_spcat_port')
        conectino_db = credentials('connection_db_spcat')
    }

    stages {
        stage('Connection to AWS server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    remote.allowAnyHosts = true
                    remote.identityFile = ssh_key
                    remote.user = ssh_key_USR
                    remote.name = server_name
                    remote.host = server_host

                    sh 'echo "$conectino_db"'
                    
                }
            }
        }

        stage('Verify Api folder and environment') {
            steps {
                script {

                    def algo = 'echo "${conectino_db}"'
                    
                    sshCommand remote: remote, command: '''
                        source ~/.bashrc
                        . ~/.bashrc
                        
                        # Verify and create the api_SPCAT folder if it does not exist and the virtual environment
                        env

                        echo $SHELL
                    '''
                    sshCommand remote: remote, command: "echo ${algo}"
                }
            }
        }

        /* stage('Verify Api folder and environment') {
            steps {
                script {
                    
                    sshCommand remote: remote, command: '''
                        # Verify and create the api_SPCAT folder if it does not exist and the virtual environment
                        if [ ! -d api_SPCAT ]; then
                            mkdir ./api_SPCAT
                            cd ./api_SPCAT
                            python3 -m venv env
                        fi
                    '''
                    
                }
            }
        }
        
        stage('Stop previous API') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Stop the API if it is running
                        
                        cd ./api_SPCAT

                        if [ -f pid.txt ]; then
                            PID_API_SPCAT=$(cat pid.txt)
                            if kill -0 "$PID_API_SPCAT" 2>/dev/null; then
                                echo "The process exists, stopping it..."
                                kill "$PID_API_SPCAT"
                            fi
                        fi
                    '''
                }
            }
        }
        
        stage('Backup previous files') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Saving old API files
                        cd ./api_SPCAT
                        rm -rf api_antiguo
                        if [ -d api_actual ]; then
                            mv api_actual api_antiguo
                        fi
                    '''
                }
            }
        }
        
        stage('Download latest release') {
            steps {
                script {
                    sshCommand remote: remote, command: '''
                        # Download the latest release from GitHub
                        cd ./api_SPCAT
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
                    sshCommand remote: remote, command: '''
                        cd ./api_SPCAT
                        # Activate the virtual environment
                        source env/bin/activate
                        
                        # Updating the dependencies
                        pip install --upgrade setuptools wheel
                        pip install -r api_actual/requirements.txt
                    '''
                }
            }
        }
        
        stage('Start API') {
            steps {
                script {
                    def port = port_api
                    sshCommand remote: remote, command: '''
                        cd ./api_SPCAT
                        # Activate the virtual environment
                        source env/bin/activate

                        cd ./api_actual

                        env

                        export DEBUG=false
                        export API_SPCAT_PORT=5000
                        export CONNECTION_DB=mongodb://AdminSpcat:Spc4t-AdmindB6@localhost:27017/spcat_db?authSource=admin

                        env

                        # Start API
                        nohup python3 api.py > api_spcat.log 2>&1 &
                        
                        # Get the new PID and save it to a file
                        PID_API_SPCAT=$!
                        echo $PID_API_SPCAT > ../pid.txt
                    '''
                }
            }
        } */
    }

    /* post {
        failure {
            script {
                sshCommand remote: remote, command: '''
                    # Rollback to the previous API if any step fails
                    cd ./api_SPCAT
                    rm -rf api_actual
                    mv api_antiguo api_actual

                    cd ./api_actual
                    source env/bin/activate

                    nohup gunicorn api:app > api_spcat.log 2>&1 &
                    PID_API_SPCAT=$!
                    echo $PID_API_SPCAT > ../pid.txt
                '''
            }
        }
    } */
}