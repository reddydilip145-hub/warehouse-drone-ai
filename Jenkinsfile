pipeline {
  agent any

  environment {
    GCP_PROJECT = 'model-journal-431911-h3'
    GKE_CLUSTER = 'fraud-cluster'
    GKE_ZONE = 'asia-south1-a'
    K8S_NAMESPACE = 'warehouse-drone-ai'
    HELM_RELEASE = 'warehouse-drone-ai'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Smoke Test') {
      steps {
        bat 'python scripts\\smoke_test.py'
      }
    }

    stage('GKE Context') {
      steps {
        bat 'gcloud config set project %GCP_PROJECT%'
        bat 'gcloud container clusters get-credentials %GKE_CLUSTER% --zone %GKE_ZONE% --project %GCP_PROJECT%'
        bat 'kubectl get nodes'
      }
    }

    stage('Build Images') {
      steps {
        bat 'gcloud builds submit --config infra\\cloudbuild\\inspection-api.yaml .'
        bat 'gcloud builds submit --config infra\\cloudbuild\\replenishment-api.yaml .'
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

