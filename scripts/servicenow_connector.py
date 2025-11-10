#!/usr/bin/env python3
"""Small ServiceNow connector to create incident tickets from alerts.

Environment variables supported:
  SERVICENOW_INSTANCE (e.g. devXXXXX.service-now.com)
  SERVICENOW_USER / SERVICENOW_PASS  OR SERVICENOW_TOKEN

Usage:
  python scripts/servicenow_connector.py --summary "Critical alert" --desc "details" --severity 1
"""
import os
import requests
import argparse
import json


def create_incident(summary: str, description: str, severity: int = 3, caller: str = 'automation'):
    instance = os.getenv('SERVICENOW_INSTANCE')
    if not instance:
        raise RuntimeError('SERVICENOW_INSTANCE env required')

    base = f'https://{instance}/api/now/table/incident'
    headers = {'Content-Type': 'application/json'}
    # prefer bearer token
    token = os.getenv('SERVICENOW_TOKEN')
    auth = None
    if token:
        headers['Authorization'] = f'Bearer {token}'
    else:
        user = os.getenv('SERVICENOW_USER')
        pwd = os.getenv('SERVICENOW_PASS')
        if not user or not pwd:
            raise RuntimeError('Provide SERVICENOW_TOKEN or SERVICENOW_USER+SERVICENOW_PASS')
        auth = (user, pwd)

    payload = {
        'short_description': summary,
        'description': description,
        'severity': str(severity),
        'caller_id': caller,
    }
    resp = requests.post(base, headers=headers, auth=auth, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--summary', '-s', required=True)
    p.add_argument('--desc', '-d', default='')
    p.add_argument('--severity', type=int, default=3)
    args = p.parse_args()
    r = create_incident(args.summary, args.desc, args.severity)
    print(json.dumps(r, indent=2))


if __name__ == '__main__':
    main()
