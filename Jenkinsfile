pipeline {
  agent any

  environment {
    GCP_PROJECT = 'model-journal-431911-h3'
    GKE_CLUSTER = 'fraud-cluster'
    GKE_ZONE = 'asia-south1-a'
    GKE_REGION = 'asia-south1'
    K8S_NAMESPACE = 'warehouse-drone-ai'
    HELM_RELEASE = 'warehouse-drone-ai'
    PYTHON_EXE = 'C:\\Program Files (x86)\\Google\\Cloud SDK\\google-cloud-sdk\\platform\\bundledpython\\python.exe'
    GCLOUD = 'C:\\Program Files (x86)\\Google\\Cloud SDK\\google-cloud-sdk\\bin\\gcloud.cmd'
    PATH = 'C:\\Program Files (x86)\\Google\\Cloud SDK\\google-cloud-sdk\\bin;C:\\Program Files\\Docker\\Docker\\resources\\bin;C:\\Windows\\System32;C:\\Windows;C:\\Windows\\System32\\WindowsPowerShell\\v1.0'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Smoke Test') {
      steps {
        bat '"%PYTHON_EXE%" scripts\\smoke_test.py'
      }
    }

    stage('GKE Context') {
      steps {
        bat '"%GCLOUD%" config set project %GCP_PROJECT%'
        bat '"%GCLOUD%" container clusters get-credentials %GKE_CLUSTER% --zone %GKE_ZONE% --project %GCP_PROJECT%'
        bat 'kubectl get nodes'
      }
    }

    stage('Build Images') {
      steps {
        bat '"%GCLOUD%" builds submit --region=%GKE_REGION% --default-buckets-behavior=regional-user-owned-bucket --config infra\\cloudbuild\\inspection-api.yaml .'
        bat '"%GCLOUD%" builds submit --region=%GKE_REGION% --default-buckets-behavior=regional-user-owned-bucket --config infra\\cloudbuild\\replenishment-api.yaml .'
      }
    }

    stage('Deploy With Helm') {
      steps {
        bat 'kubectl apply -f infra\\kubernetes\\namespaces\\warehouse-drone-ai.yaml'
        bat 'helm upgrade --install %HELM_RELEASE% infra\\helm\\warehouse-drone-ai --namespace %K8S_NAMESPACE%'
      }
    }

    stage('Verify Rollout') {
      steps {
        bat 'kubectl rollout status deployment/inspection-api -n %K8S_NAMESPACE% --timeout=180s'
        bat 'kubectl rollout status deployment/replenishment-api -n %K8S_NAMESPACE% --timeout=180s'
        bat 'kubectl get pods -n %K8S_NAMESPACE%'
      }
    }
  }

  post {
    always {
      bat 'kubectl get svc -n %K8S_NAMESPACE% || exit /b 0'
    }
  }
}
