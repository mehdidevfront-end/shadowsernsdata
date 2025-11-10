#!/usr/bin/env python3
"""Azure connector using MSAL to authenticate and query Resource Graph.

Requirements:
  pip install msal requests

Usage (environment variables or args):
  python scripts/azure_connector.py --client-id <id> --client-secret <secret> --tenant <tenant>

The script outputs a standardized JSON list of resources: id, name, type, location, subscriptionId, tags
"""
import argparse
import os
import json
import msal
import requests


RESOURCE = "https://management.azure.com/.default"
RG_ENDPOINT = "https://management.azure.com/providers/Microsoft.ResourceGraph/resources?api-version=2021-03-01"


def get_token(client_id, client_secret, tenant_id):
    app = msal.ConfidentialClientApplication(
        client_id, authority=f"https://login.microsoftonline.com/{tenant_id}", client_credential=client_secret
    )
    result = app.acquire_token_for_client(scopes=[RESOURCE])
    if "access_token" in result:
        return result["access_token"]
    raise RuntimeError(f"Failed to acquire token: {result}")


def query_resource_graph(token, query="Resources | project id, name, type, location, subscriptionId, tags"):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"query": query}
    resp = requests.post(RG_ENDPOINT, headers=headers, json=body)
    resp.raise_for_status()
    return resp.json()


def normalize(results):
    # Resource Graph returns a 'data' -> 'rows' with columns in 'columns'
    out = []
    cols = [c['name'] for c in results.get('columns', [])]
    for row in results.get('data', {}).get('rows', []):
        obj = {cols[i]: row[i] for i in range(min(len(cols), len(row)))}
        out.append(obj)
    return out


def main(args):
    client_id = args.client_id or os.getenv('AZ_CLIENT_ID')
    client_secret = args.client_secret or os.getenv('AZ_CLIENT_SECRET')
    tenant = args.tenant or os.getenv('AZ_TENANT_ID')
    if not (client_id and client_secret and tenant):
        raise SystemExit('Missing credentials; set AZ_CLIENT_ID/AZ_CLIENT_SECRET/AZ_TENANT_ID or pass args')

    token = get_token(client_id, client_secret, tenant)
    raw = query_resource_graph(token, query=args.query)
    items = normalize(raw)
    print(json.dumps({'collected_at': __import__('datetime').datetime.utcnow().isoformat() + 'Z', 'resources': items}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--client-id')
    p.add_argument('--client-secret')
    p.add_argument('--tenant')
    p.add_argument('--query', default='Resources | project id, name, type, location, subscriptionId, tags')
    args = p.parse_args()
    main(args)
