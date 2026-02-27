# Task 2 — CI/CD Pipeline

This section contains CI workflows and GitOps manifests to build, test, scan, and deploy the Task 1 app.

- CI: GitHub Actions workflows under `.github/workflows/` (for real GitHub runs)
- GitOps: Argo CD app + Kustomize overlays under `task-2-cicd/gitops/` (to be implemented)

## Implemented so far

- GitHub Actions workflow: `.github/workflows/task1-ci.yml`
  - Runs API tests (pytest) for `task-1-kubernetes/app/api`
  - Builds Docker images for API and frontend
  - Includes commented-out steps for pushing images to a container registry
