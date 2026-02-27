# Running locally with Kind

## Prerequisites

- Docker Desktop
- `kind`, `kubectl`, `helm`

## 1) Create cluster

```bash
kind create cluster --name dodo-assessment
```

## 2) Install NGINX Ingress Controller

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

## 3) Build and load images

From the repository root:

```bash
# API
docker build -t dodo-api:local task-1-kubernetes/app/api

# Frontend
docker build -t dodo-frontend:local task-1-kubernetes/app/frontend

# Load into Kind cluster
kind load docker-image dodo-api:local --name dodo-assessment
kind load docker-image dodo-frontend:local --name dodo-assessment
```

## 4) Deploy the app

```bash
kubectl apply -k ../k8s/overlays/dev
```

## 5) Access

When using Kind, expose ingress-nginx via port-forward:

```bash
kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8080:80
```

Then open:

- Frontend: `http://localhost:8080/`
- API health: `http://localhost:8080/api/healthz`

