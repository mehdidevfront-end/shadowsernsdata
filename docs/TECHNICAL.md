# Technical Documentation (summary)

This document summarizes the repository architecture, APIs, IA model, storage, and how to run the E2E demo.

## Overview

- Frontend: Next.js + Tailwind. Pages: Graph view (`/graph/[asset]`), Anomalies dashboard (`/anomalies`), Compliance (`/compliance`), FinOps (`/finops`), Chat (`/chat`).
- Backend: FastAPI (backend/app). Endpoints:
  - `GET /graph/{asset}` - returns incoming/outgoing DEPENDS_ON neighbours from Neo4j (supports query params: `type`, `criticite`, `bu`, `env`).
  - `GET /assets`, `POST /assets`, `PUT /assets/{id}` - assets CRUD (file-backed in `backend_data/assets.json`).
  - `GET /risks`, `POST /risks`, `PUT /risks/{id}` - risks CRUD (file-backed `backend_data/risks.json`).
  - `GET /compliance` - sample KPIs.
  - `GET /finops` - sample FinOps KPIs.
  - `POST /qa` - retrieval + LLM endpoint (queries OpenSearch then calls configured LLM).

## IA Model

- Data prep: `scripts/prepare_dataset.py` reads JSONL logs and outputs cleaned JSONL (`hour`, `dow`, `is_saas`, anonymized IPs, hashed ids).
- Shadow scan: `scripts/shadow_scan.py` detects SaaS exposures using `scripts/saas_regex_engine.py` and writes `reports/shadow_report.jsonl`.
- Training: `scripts/train_autoencoder.py` trains a small PyTorch autoencoder on cleaned data and writes `models/autoencoder.pt`, `models/scaler.joblib`, and `models/threshold.json`.
- Prediction: `scripts/predict_anomaly.py` computes reconstruction error per record and outputs `predictions.jsonl`.
- Alerting: `scripts/alerting.py` can read predictions and send Slack alerts (needs `SLACK_WEBHOOK_URL`).

## Retrieval (OpenSearch)

- Index contexts for retrieval with `scripts/index_retrieval.py --input contexts.jsonl --index llm_contexts`.
- The `POST /qa` endpoint uses OpenSearch to retrieve top-k contexts and then calls an LLM (OpenAI if `OPENAI_API_KEY` set). Adjust `OPENSEARCH_URL` env var.

## ServiceNow integration

- `scripts/servicenow_connector.py` can create incidents via ServiceNow REST API (requires `SERVICENOW_INSTANCE` and token or username/password). You can call it from alerting scripts to auto-create tickets.

## Reporting

- Weekly Airflow DAG: `airflow/dags/reporting_weekly.py` runs `airflow/dags/scripts/generate_pdf_report.py` to create a PDF (`reports/weekly_report_<date>.pdf`) and optionally upload to MinIO (requires `minio` client and `MINIO_*` env vars).

## File storage

- Lightweight file-backed storage in `backend_data/` (assets.json, risks.json). For production, migrate to a DB (Postgres / SQLModel).

## How to run the E2E demo locally (quick)

1. Ensure Python deps installed (see repository `requirements.txt` or install minimal packages):
   - requests, opensearch-py, reportlab, minio, joblib, scikit-learn, torch (optional for training).
2. From repo root run the demo orchestrator:
   ```bash
   bash scripts/run_e2e_demo.sh
   ```
   This script will create sample allowed SaaS, produce sample logs, run `shadow_scan`, prepare dataset, train a tiny autoencoder, predict anomalies and write results in `predictions.jsonl`.

## Notes & Next steps

- Add persistent datastore (Postgres/SQLModel) and background workers for long-running tasks.
- Add proper CI tests (pytest) for endpoints and small integration tests mocking Neo4j/OpenSearch.
- Harden security (secrets, CORS, auth) before exposing services.

-- End of summary
