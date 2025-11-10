#!/usr/bin/env python3
"""Alerting helper: read predictions JSONL and send Slack alerts for anomalies above threshold.

Requires environment variable SLACK_WEBHOOK_URL or pass --webhook.

Usage:
  python3 scripts/alerting.py --pred predictions.jsonl --webhook <url> --severity-threshold 0.8
"""
import argparse
import json
import os
import requests


def send_slack(webhook, text, attachments=None):
    payload = {'text': text}
    if attachments:
        payload['attachments'] = attachments
    resp = requests.post(webhook, json=payload, timeout=10)
    return resp.status_code, resp.text


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pred', '-p', required=True, help='predictions JSONL')
    p.add_argument('--webhook', '-w', help='Slack webhook URL (or set SLACK_WEBHOOK_URL env)')
    p.add_argument('--threshold', type=float, default=None, help='threshold to trigger alert (optional)')
    args = p.parse_args()

    webhook = args.webhook or os.getenv('SLACK_WEBHOOK_URL')
    if not webhook:
        print('No webhook provided; set SLACK_WEBHOOK_URL or pass --webhook')
        return

    with open(args.pred, encoding='utf-8') as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except Exception:
                continue
            score = rec.get('anomaly_score')
            is_anom = rec.get('anomaly')
            if is_anom or (args.threshold is not None and score is not None and score > args.threshold):
                text = f"Anomaly detected (score={score}): {rec.get('record', {}).get('ts') or 'unknown ts'}"
                send_slack(webhook, text)

    print('Alerting run completed')


if __name__ == '__main__':
    main()
