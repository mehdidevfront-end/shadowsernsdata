#!/usr/bin/env bash
# Simple E2E demo script: runs shadow_scan -> prepare_dataset -> train -> predict
set -euo pipefail
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

echo "1) Generate allowed_saas sample"
python3 scripts/list_allowed_saas.py --output config/allowed_saas.json

echo "2) Ensure reports and data dirs exist"
mkdir -p reports data models

echo "3) Run shadow scan on sample logs"
python3 scripts/shadow_scan.py --log logs/sample_logs.jsonl --allowed config/allowed_saas.json --out reports/shadow_report.jsonl

echo "4) Prepare dataset"
python3 scripts/prepare_dataset.py --in reports/shadow_report.jsonl --out data/cleaned.jsonl --allowed config/allowed_saas.json

echo "5) Train tiny autoencoder (5 epochs)"
python3 scripts/train_autoencoder.py --in data/cleaned.jsonl --out models --epochs 5

echo "6) Predict anomalies"
python3 scripts/predict_anomaly.py --model models/autoencoder.pt --scaler models/scaler.joblib --in data/cleaned.jsonl --out predictions.jsonl --threshold models/threshold.json

echo "E2E demo finished. Outputs: reports/shadow_report.jsonl data/cleaned.jsonl models/ predictions.jsonl"
