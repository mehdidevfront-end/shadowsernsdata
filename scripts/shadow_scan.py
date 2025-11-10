#!/usr/bin/env python3
"""Shadow scan: read logs (jsonl or text) and detect SaaS usage and anomalies.

Produces a JSON report with entries: timestamp, source_line, detections, fields...

Usage:
  python scripts/shadow_scan.py --log logs/app.log --out reports/shadow_report.jsonl --allowed config/allowed_saas.json
"""
import argparse
import json
import os
import re
from datetime import datetime

from saas_regex_engine import load_allowed_saas, build_patterns, detect_saas


def try_parse_json_line(line):
    try:
        return json.loads(line)
    except Exception:
        return None


def extract_text_from_record(rec):
    # try common fields
    for f in ('message', 'msg', 'request', 'url', 'payload', 'body'):
        if f in rec and isinstance(rec[f], str):
            return rec[f]
    # fallback to entire JSON
    return json.dumps(rec)


def normalize_ts(rec):
    # try common timestamp fields
    for f in ('timestamp', 'time', '@timestamp', 'ts'):
        if f in rec:
            v = rec[f]
            try:
                # try ISO format
                return datetime.fromisoformat(v).isoformat()
            except Exception:
                try:
                    # numeric epoch
                    return datetime.utcfromtimestamp(float(v)).isoformat()
                except Exception:
                    return str(v)
    return None


def scan_file(path, patterns):
    with open(path, encoding='utf-8', errors='ignore') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = try_parse_json_line(line)
            if rec:
                text = extract_text_from_record(rec)
                ts = normalize_ts(rec)
            else:
                text = line
                ts = None
            detections = detect_saas(text, patterns)
            if detections:
                out = {
                    'timestamp': ts,
                    'detections': detections,
                    'source': path,
                    'line': line if len(line) < 2000 else line[:2000],
                }
                yield out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--log', '-l', required=True, help='Log file to scan (text or jsonl)')
    p.add_argument('--allowed', '-a', help='allowed_saas JSON file (optional)')
    p.add_argument('--out', '-o', default='reports/shadow_report.jsonl')
    args = p.parse_args()

    allowed = None
    if args.allowed:
        allowed = load_allowed_saas(args.allowed)
    patterns = build_patterns(allowed)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as outfh:
        for hit in scan_file(args.log, patterns):
            outfh.write(json.dumps(hit, ensure_ascii=False) + '\n')

    print('Wrote report to', args.out)


if __name__ == '__main__':
    main()
