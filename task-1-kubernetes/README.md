# Task 1 — Kubernetes Cluster Setup & Microservices Deployment

Goal: deploy a small microservices app to Kubernetes demonstrating core orchestration primitives.

## What’s included (in this repo)

- **Frontend**: static web UI served by NGINX (calls the API)
- **API**: FastAPI service (Python) with health endpoints and DB connectivity
- **Database**: PostgreSQL (StatefulSet + PVC)

Kubernetes resources:

- Deployments/StatefulSet, Services, ConfigMaps, Secrets, Ingress
- Resource requests/limits for all containers
- Liveness/readiness probes for all services
- HPA for the API
- Bonus: NetworkPolicies + PodDisruptionBudgets

## How to run (Kind + NGINX Ingress)

See `task-1-kubernetes/docs/kind.md`.

