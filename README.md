# Ecommerce Platform

High-load e-commerce backend built with FastAPI, PostgreSQL, and Redis.

## Environments

| Env | Env file | DB | Debug | Error details |
|-----|----------|-----|-------|---------------|
| dev | `configs/.env` | `localhost:5434/ecom_dev` | on | shown |
| sandbox | `configs/.env.sandbox` | `localhost:5435/ecom_sandbox` | on | shown |
| production | `configs/.env.production` | `localhost:5436/ecom_prod` | off | hidden |

## Setup (once)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pre-commit && pre-commit install
```

## Run — Sandbox

```powershell
docker compose up -d postgres-sandbox redis
$env:APP_ENV="sandbox"
python -m scripts.init_db
python -m scripts.seed_admin
uvicorn src.main:app --reload --port 8000
```

Open <http://127.0.0.1:8000/docs>.

## Run — Production (locally simulated)

```powershell
docker compose up -d postgres-prod redis
$env:APP_ENV="production"
python -m scripts.init_db
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Tests

```powershell
pytest -v
```

## Deployment

Production runs on **Render**: <https://ecommerce-platform.onrender.com>

Environment variables are configured in the Render dashboard (see `configs/.env.example` for the required keys). Real values are never committed.