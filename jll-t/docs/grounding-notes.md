# Grounding Notes

This document records the architectural patterns that informed the falcon-grounds scaffold.

## Patterns Used

### Container Base Image
Python 3.12-slim is the base image. The `-slim` variant removes build tools and test
packages, reducing image size by roughly 70% compared to the full python:3.12 image.
This is a standard practice for production Python services.

### Non-Privileged Container User
The application runs as `appuser` with UID 10001, created by the Dockerfile before
the application code is copied. This follows the principle of least privilege and is
required by many enterprise container policies (AKS, Azure Container Apps).

### FastAPI on Port 8000
FastAPI with uvicorn is the de-facto standard for async Python APIs. Port 8000 is the
conventional development port. The lifespan context manager handles startup and
shutdown tasks (schema initialization, connection pool draining).

### Docker Compose for Local Orchestration
Three services: postgres (pgvector image), redis (alpine), and the API. Health checks
on postgres and redis prevent the API from starting before its dependencies are ready.
Named volumes preserve data across `docker compose restart`.

### pyproject.toml with Hatchling
PEP 517 build system. Hatchling is a minimal, fast build backend. The `src/` layout
keeps application code out of the repository root, preventing accidental imports from
the wrong path.

### PYTHONDONTWRITEBYTECODE and PYTHONUNBUFFERED
`PYTHONDONTWRITEBYTECODE=1` prevents `.pyc` file creation in the container, reducing
image size and avoiding stale bytecode issues. `PYTHONUNBUFFERED=1` ensures log output
is written to stdout immediately, which is required for container log aggregation.

### src/ Layout
Application code lives under `src/falcon_grounds/`. This prevents the package from
being importable without installation and avoids path collisions between the package
and top-level scripts.

### JSONL Append-Only Logs
Audit events and cost entries are written as newline-delimited JSON. JSONL is
trivially writable (append-only), parseable line-by-line without loading the full
file, and compatible with tools like `jq`, BigQuery, and Azure Log Analytics.

### Environment-Based Runtime Mode Switching
Three modes (local, hybrid, cloud) are selected via `RUNTIME_MODE` environment variable.
All external clients check this flag at construction time. Switching between modes
requires only environment variable changes, not code changes.

## Notes on Source

No proprietary code or client data was used in this scaffold. All patterns are
standard open-source and cloud-native practices documented in official Python,
FastAPI, Docker, and Azure documentation.
