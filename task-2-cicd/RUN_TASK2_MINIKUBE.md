## Task 2 — CI/CD (Minikube + GitHub Actions + Argo CD)

This guide runs Task 2 end-to-end:

- **CI**: GitHub Actions runs tests + builds images and (optionally) pushes to GHCR
- **CD/GitOps**: Argo CD pulls manifests from Git and deploys to your Minikube cluster

### A. CI (GitHub Actions)

#### A1) Ensure your workflow is in the repo

Workflow file:

- `.github/workflows/task1-ci.yml`

Push your code to GitHub and confirm the workflow appears under GitHub → **Actions**.

#### A2) Trigger CI

Make any small change under `task-1-kubernetes/**`, commit, and push. This triggers CI.

#### A3) (Optional) Push images to GHCR

The GitOps overlay `task-1-kubernetes/k8s/overlays/gitops` expects images:

- `ghcr.io/lavanyachamarthi24/devops_projects/dodo-api:latest`
- `ghcr.io/lavanyachamarthi24/devops_projects/dodo-frontend:latest`

Enable image push steps in the workflow (if you want fully automated CD with registry images) and ensure GitHub Actions has permission to publish packages (GHCR).

### B. CD / GitOps (Argo CD on Minikube)

#### B1) Install Argo CD

```powershell
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait for Argo CD pods:

```powershell
kubectl get pods -n argocd -w
```

#### B2) Open the Argo CD UI

Port-forward the Argo CD API server:

```powershell
kubectl -n argocd port-forward svc/argocd-server 8081:443
```

Open:

- `https://localhost:8081`

#### B3) Get the admin password

```powershell
$pwd = kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}"
[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($pwd))
```

Username is:

- `admin`

#### B4) Create the GitOps Application

Apply the Argo CD `Application` manifest from this repo:

```powershell
kubectl apply -f task-2-cicd/gitops/argocd/application-task1.yaml
```

Then check sync status:

```powershell
kubectl get applications -n argocd
```

In Argo CD UI, you should see `task1-microservices` and it should sync/health to **Healthy**.

#### B5) Access the deployed app

Task 1 ingress uses host `dodo.local`.

- Ensure your Windows `hosts` file contains:

```text
127.0.0.1 dodo.local
```

Expose the ingress controller:

```powershell
kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8080:80
```

Open:

- `http://dodo.local:8080/`
- `http://dodo.local:8080/api/healthz`

### Notes / Troubleshooting

- If Argo CD shows image pull errors, confirm your CI pushed images to GHCR **or** update the overlay to reference images your cluster can pull.
- If your GitHub repo is private, Argo CD must be configured with repo credentials (SSH key or token) before it can sync.

