
pipeline {
    agent any
    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }
    // Jenkins must be running to poll. The first build can be started manually.
    triggers {
        pollSCM('H/2 * * * *')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Docker availability') {
            steps {
                sh 'docker version'
            }
        }
        stage('Build test image') {
            steps {
                sh 'docker build --target test -t cyberquality-static-assessor:test-${BUILD_NUMBER} .'
            }
        }
        stage('Unit tests') {
            steps {
                sh 'docker run --rm cyberquality-static-assessor:test-${BUILD_NUMBER} python -m pytest -q tests'
            }
        }
        stage('Build application image') {
            steps {
                sh 'docker build --target runtime -t cyberquality-static-assessor:${BUILD_NUMBER} .'
            }
        }
        stage('Image smoke test') {
            steps {
                sh '''
                    docker run --rm --entrypoint python \
                      cyberquality-static-assessor:${BUILD_NUMBER} \
                      -c 'import cyberquality; import streamlit; print("Imports OK")'
                '''
            }
        }
    }
    post {
        success {
            echo 'CI passed: tests, application image build and import smoke test.'
        }
        failure {
            echo 'CI failed: open Console Output and check the first failing stage.'
        }
    }
}
