#!/usr/bin/env python3
"""Extract allowed SaaS from an ITSM CSV/JSON export and produce a normalized JSON reference.

Usage:
  python scripts/list_allowed_saas.py --input itsm_export.csv --output config/allowed_saas.json

If no input provided, writes a small example file to `config/allowed_saas.json`.
"""
import argparse
import csv
import json
import os


def read_csv(path):
    items = []
    with open(path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            name = row.get('name') or row.get('Name') or row.get('service') or row.get('Service')
            domains = (row.get('domains') or row.get('domain') or row.get('Domains') or '')
            tags = (row.get('tags') or row.get('Tags') or '')
            owner = row.get('owner') or row.get('Owner') or ''
            items.append({
                'name': name.strip() if name else None,
                'domains': [d.strip() for d in domains.split(';') if d.strip()],
                'tags': [t.strip() for t in tags.split(',') if t.strip()],
                'owner': owner.strip(),
            })
    return items


def read_json(path):
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    # expect list of objects or dict
    if isinstance(data, dict):
        # try common key
        data = data.get('items') or data.get('services') or [data]
    return data


DEFAULT_SAMPLE = [
    {"name": "Dropbox", "domains": ["dropbox.com"], "tags": ["file-sharing"], "owner": "IT"},
    {"name": "Zoom", "domains": ["zoom.us", "zoom.com"], "tags": ["video"], "owner": "Comms"},
    {"name": "Slack", "domains": ["slack.com"], "tags": ["chat"], "owner": "Comms"},
    {"name": "Google Drive", "domains": ["drive.google.com", "docs.google.com"], "tags": ["file-sharing"], "owner": "IT"},
    {"name": "OneDrive", "domains": ["onedrive.live.com"], "tags": ["file-sharing"], "owner": "IT"},
    {"name": "Salesforce", "domains": ["salesforce.com"], "tags": ["crm"], "owner": "Sales"},
]


def write_json(path, items):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(items, fh, indent=2, ensure_ascii=False)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', '-i', help='ITSM export CSV or JSON')
    p.add_argument('--output', '-o', default='config/allowed_saas.json')
    args = p.parse_args()

    if not args.input:
        print('No input provided; writing sample allowed_saas to', args.output)
        write_json(args.output, DEFAULT_SAMPLE)
        return

    if args.input.lower().endswith('.csv'):
        items = read_csv(args.input)
    else:
        items = read_json(args.input)

    # normalize domains and remove empties
    for it in items:
        if 'domains' in it and isinstance(it['domains'], str):
            it['domains'] = [d.strip() for d in it['domains'].split(';') if d.strip()]

    write_json(args.output, items)
    print('Wrote', len(items), 'entries to', args.output)


if __name__ == '__main__':
    main()
