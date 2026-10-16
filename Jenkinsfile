pipeline {
    agent any
    // Agent prerequisite: JDK 25 on PATH (Maven 3.9.16 comes from case-study/mvnw). No automatic plugin/tool provisioning.
    stages {
        stage('Test') {
            steps { sh 'case-study/mvnw -B -ntp -f case-study/pom.xml clean test' }
        }
        stage('Coverage gate') {
            steps { sh 'case-study/mvnw -B -ntp -f case-study/pom.xml clean verify' }
        }
        stage('Package') {
            steps { sh 'case-study/mvnw -B -ntp -f case-study/pom.xml -DskipTests package' }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, testResults: 'case-study/target/surefire-reports/TEST-*.xml'
            archiveArtifacts allowEmptyArchive: true, artifacts: 'case-study/target/site/jacoco/**,case-study/target/*.jar'
        }
    }
}
