pipeline {
    agent {
        node {
            label 'Dev-Node'
        }
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
        stage("Dockerhub push"){
            steps{
                withCredentials(
                    [
                        usernamePassword(
                            credentialsId:"dockerhub_cred",
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
