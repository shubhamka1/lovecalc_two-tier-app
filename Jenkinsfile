pipeline {
        agent {
            node {
                label 'Dev-Node'
            }
        }

        environment{
            SONAR_VAR= tool "sonarqube_scanner"
        }

    stages {
        stage("GIT code clone") {
            steps {
                git url: "https://github.com/shubhamka1/lovecalc_two-tier-app.git", branch: "master"
                echo "Code is cloned"
            }
        }
        stage("create docker network and volume"){
            steps{
                /*sh "docker network create my_net"
                sh "docker volume create mysql-data"*/
                echo "created network and volume"
            }
            
        }
        stage("clear docker ps")
        {
            steps{
                script{
                    def runningcontainer = sh(script:'docker ps -q | grep -v sonarqube', returnStdout: true).trim()
                    if(runningcontainer){
                        sh 'docker stop $(docker ps | grep -v sonarqube | awk '{print $1}')'
                    }
                    
                    def removecontainer= sh(script:'docker ps -aq',returnStdout: true).trim()
                    if(removecontainer){
                        sh 'docker rm $(docker ps -a | grep -v sonarqube | awk '{print $1}')'
                    }

                    def removeimages= sh(script:'docker images -q', returnStdout: true).trim()
                    if(removeimages){
                        sh 'docker rmi $(docker images -a | grep -v sonarqube | awk '{print $3}')'
                    }
                }

                
            }
        }
        stage("running database"){
            steps{
                sh "whoami"
                sh "docker run -d --name mysql_appdb --network my_net -v mysql-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=love_calculator mysql:5.7"
            }
        }
        stage("Build and run Docker containers") {
            steps {
                sh 'docker build -t love_calc:latest .'
                sh 'docker run -d --name love_calc_app_node --network my_net -p 5000:5000 -e DB_HOST=mysql_appdb -e DB_USER=root -e DB_PASSWORD=root -e DB_NAME=love_calculator love_calc:latest'
                echo "Application is up and running. Please open it in your browser."
            }
        }

        stage("Sonar-qube analysis"){
            steps{
                /* here withSonarQube is jenkin pipline step provided by the SonarQube Scanner for Jenkins plugin 
                we specify the Sonarqube server name that we configured in jenkins , then in environments we specified sonar-scanner tool. 
                so that is used here to send code in compressed format with project name and project key as ENV variable sonar-scanner is command 
                present in tools /bin/ folder */
                withSonarQubeEnv("Sonarqube"){
                    sh "$SONAR_VAR/bin/sonar-scanner -Dsonar.projectName=love-calc-two-tier -Dsonar.projectKey=love-calc"
                }
            }
        }

        stage("Sonar-qube quality gate"){
            steps{
                echo "quality gates check"
            }
        }



        stage("Dockerhub push"){
            steps{
                withCredentials(
                    [
                        usernamePassword(
                            credentialsId:"dockerhub_creds",
                            usernameVariable:"dockerhubUser",
                            passwordVariable:"dockerhubPass"
                            )
                    ]
                        
                ){
                     echo "username is $dockerhubUser"
                     sh "docker tag love_calc:latest $dockerhubUser/love_calc:latest"
                     sh "docker login -u $dockerhubUser -p $dockerhubPass"
                     sh "docker push $dockerhubUser/love_calc:latest"
                }
            }
        }
        stage("Check application") {
            steps {
                // Add appropriate steps to check the application here
                echo "Checking the application..."
            }
        }
    }
}
