import os
import time

import psycopg
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = FastAPI(title="dodo-api", version="1.0.0")

REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["path"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)


def _db_dsn() -> str:
    host = os.getenv("DB_HOST", "postgres")
    port = int(os.getenv("DB_PORT", "5432"))
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    db = os.getenv("DB_NAME", "app")
    sslmode = os.getenv("DB_SSLMODE", "disable")
    return f"host={host} port={port} user={user} password={password} dbname={db} sslmode={sslmode}"


def _db_ping(timeout_s: float = 1.0) -> bool:
    try:
        with psycopg.connect(_db_dsn(), connect_timeout=timeout_s) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return True
    except Exception:
        return False


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz(response: Response):
    if not _db_ping():
        response.status_code = 503
        return {"status": "not-ready"}
    return {"status": "ready"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from dodo-api"}


@app.get("/api/time")
def api_time():
    return {"unix": int(time.time())}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    path = request.url.path

    LATENCY.labels(path=path).observe(duration)
    REQUESTS.labels(method=request.method, path=path, status=str(response.status_code)).inc()
    return response

