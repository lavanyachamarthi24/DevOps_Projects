## Task 1 — Run Locally with Minikube

This guide documents how to run the Task 1 microservices app (frontend, API, PostgreSQL) locally using **Minikube** and **NGINX Ingress** on Windows.

### 1. Prerequisites

- **Windows 10+**
- **Docker Desktop** installed and running
- **kubectl** installed (`kubectl version --client`)
- **Minikube** installed (`minikube version`)
- **NGINX ingress addon** (enabled later in this guide)

If Minikube is not installed, on PowerShell (as Administrator) you can use one of:

- With Chocolatey:

```powershell
choco install -y minikube
```

- With Winget:

```powershell
winget install -e --id Kubernetes.minikube
```

### 2. Clone and enter the repository

Open **PowerShell** and go to the repo root:

```powershell
cd "C:\Users\Admin\Downloads\Dodo_Assessment"
```

Adjust the path if your checkout is elsewhere.

### 3. Start Minikube

Start Minikube (using Docker as the driver is typical on Windows):

```powershell
minikube start --driver=docker
```

Verify the cluster is up:

```powershell
kubectl get nodes
```

### 4. Enable NGINX Ingress

Enable the built-in ingress addon:

```powershell
minikube addons enable ingress
```

Confirm the ingress controller is running:

```powershell
kubectl get pods -n ingress-nginx
```

### 5. Build Docker images

From the repo root, build the API and frontend images with the tags expected by the Kubernetes manifests (`dodo-api:local` and `dodo-frontend:local`):

```powershell
cd "C:\Users\Admin\Downloads\Dodo_Assessment"

docker build -t dodo-api:local task-1-kubernetes/app/api
docker build -t dodo-frontend:local task-1-kubernetes/app/frontend
```

### 6. Load images into Minikube

Load the locally built images into the Minikube cluster:

```powershell
minikube image load dodo-api:local
minikube image load dodo-frontend:local
```

You can verify they are available with:

```powershell
kubectl get pods -A
```

after deployment (next step).

### 7. Deploy Task 1 manifests with Kustomize

Apply the `dev` overlay for Task 1:

```powershell
cd "C:\Users\Admin\Downloads\Dodo_Assessment"
kubectl apply -k task-1-kubernetes/k8s/overlays/dev
```

This creates:

- Namespace: `dev-dodo-app` (resources are prefixed with `dev-`)
- Deployments: API + frontend
- StatefulSet: PostgreSQL
- Services: internal ClusterIP services for API, frontend, and Postgres
- Ingress: routes `dodo.local` to frontend and API

Check the resources:

```powershell
kubectl get pods -n dodo-app
kubectl get deploy,sts,svc,ingress -n dodo-app
```

Wait until:

- `dev-postgres-0` is `1/1 Running`
- `dev-api-…` pods are `1/1 Running`
- `dev-frontend-…` pods are `1/1 Running`

If API or frontend pods show `ImagePullBackOff`, ensure you built and loaded the images (steps 5–6) and then delete the failing pods to let the Deployment recreate them:

```powershell
kubectl -n dodo-app delete pod <pod-name-1> <pod-name-2> ...
```

### 8. Configure local DNS for Ingress host

The ingress is configured for the host **`dodo.local`**. Add an entry to your Windows hosts file so the name resolves to localhost.

1. Open **Notepad as Administrator**.
2. Open `C:\Windows\System32\drivers\etc\hosts`.
3. Add this line at the end:

```text
127.0.0.1 dodo.local
```

4. Save and close.

### 9. Expose the ingress controller locally

Use `kubectl port-forward` to expose the NGINX ingress controller on your machine:

```powershell
kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8080:80
```

Leave this command running.

### 10. Access the application

With port-forwarding active and the `hosts` entry added, open a browser and go to:

- **Frontend**: `http://dodo.local:8080/`

You should see the microservices demo UI.

You can also hit the API health endpoint via ingress:

- **API health via ingress**: `http://dodo.local:8080/api/healthz`

Or port‑forward directly to the API service for debugging:

```powershell
kubectl -n dodo-app port-forward svc/dev-api 8000:8000
```

Then:

- `http://localhost:8000/healthz`
- `http://localhost:8000/api/hello`

### 11. Stopping and cleaning up

- Stop port‑forwarding: press `Ctrl+C` in the PowerShell window running `kubectl port-forward`.
- To remove the Task 1 resources:

```powershell
kubectl delete -k task-1-kubernetes/k8s/overlays/dev
```

- To stop Minikube:

```powershell
minikube stop
```

### 12. Exporting this guide to PDF

To save this document as a PDF:

1. Open `task-1-kubernetes/RUN_LOCAL_MINIKUBE.md` in your editor or a Markdown viewer.
2. Use **Print** → **Microsoft Print to PDF** (or your PDF printer of choice), or use your editor’s “Export as PDF” feature if available.
3. Save the PDF with a descriptive name, for example: `Task1_Minikube_Running_Guide.pdf`.

