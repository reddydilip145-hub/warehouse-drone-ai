# Deployment Hands-On

## Current Target

Use the existing GKE cluster:

```text
project: model-journal-431911-h3
cluster: fraud-cluster
location: asia-south1-a
namespace: warehouse-drone-ai
image registry: asia-south1-docker.pkg.dev/model-journal-431911-h3/warehouse-drone-ai
```

Kubeflow is already installed in the `kubeflow` namespace. We will deploy the application services separately first, then use Kubeflow for ML runs.

## Build Images With Cloud Build

```powershell
gcloud builds submit --config infra\cloudbuild\inspection-api.yaml .
gcloud builds submit --config infra\cloudbuild\replenishment-api.yaml .
```

## Deploy With Helm

```powershell
kubectl apply -f infra\kubernetes\namespaces\warehouse-drone-ai.yaml
helm upgrade --install warehouse-drone-ai infra\helm\warehouse-drone-ai --namespace warehouse-drone-ai
kubectl get pods -n warehouse-drone-ai
kubectl get svc -n warehouse-drone-ai
```

## Test APIs

```powershell
kubectl port-forward svc/inspection-api 8000:80 -n warehouse-drone-ai
curl http://localhost:8000/health
```

In another terminal:

```powershell
kubectl port-forward svc/replenishment-api 8001:80 -n warehouse-drone-ai
curl http://localhost:8001/health
```

## Argo CD

Install Argo CD only after Helm deployment works:

```powershell
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f infra\argocd\warehouse-drone-ai-application.yaml
```

## Kubeflow

Kubeflow is already present. Use it for the ML DAG after service deployment is stable:

```text
ml/pipelines/kubeflow_pipeline.py
```
