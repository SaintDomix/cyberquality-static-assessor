pipeline {
    agent any
    options { timestamps(); disableConcurrentBuilds(); skipDefaultCheckout(true) }
    triggers { pollSCM('H/2 * * * *') }
    environment { IMAGE_NAME = 'cyberquality-static-assessor' }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Docker availability') { steps { sh 'docker version' } }
        stage('Build test image') {
            steps { sh 'docker build --target test -t cyberquality-static-assessor:test-${BUILD_NUMBER} .' }
        }
        stage('Unit tests') {
            steps { sh 'docker run --rm cyberquality-static-assessor:test-${BUILD_NUMBER} python -m pytest -q tests --junitxml=/tmp/results.xml' }
        }
        stage('Build application image') {
            steps { sh 'docker build --target runtime -t cyberquality-static-assessor:${BUILD_NUMBER} .' }
        }
        stage('Image smoke test') {
            steps { sh 'docker run --rm --entrypoint python cyberquality-static-assessor:${BUILD_NUMBER} -c "import cyberquality; import streamlit; print("Imports OK")"' }
        }
    }
    post { success { echo 'Unit tests, image build, and import smoke test passed.' }
           failure { echo 'Inspect the failing pipeline stage in Console Output.' }
           always { cleanWs(deleteDirs: true, notFailBuild: true) } }
}
