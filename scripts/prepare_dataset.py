#!/usr/bin/env python3
"""Prepare dataset for ML: normalize timestamps, anonymize IPs, extract basic time features and label SaaS hits.

Input: JSONL logs (one JSON object per line)
Output: cleaned JSONL suitable for training (ISO timestamps, anonymized ips, features)

Usage:
  python scripts/prepare_dataset.py --in logs/jsonl --out data/cleaned.jsonl --allowed config/allowed_saas.json
"""
import argparse
import json
import ipaddress
import hashlib
from datetime import datetime

from saas_regex_engine import load_allowed_saas, build_patterns, detect_saas


def anonymize_ip(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
        if ip.version == 4:
            parts = ip_str.split('.')
            parts[-1] = '0'
            return '.'.join(parts)
        else:
            # zero the last 80 bits (keep /48)
            network = ipaddress.ip_network(ip.exploded + '/48', strict=False)
            return str(network.network_address)
    except Exception:
        return ip_str


def hash_value(val):
    return hashlib.sha1(val.encode('utf-8')).hexdigest()[:12]


def normalize_ts(rec):
    for f in ('timestamp', 'time', '@timestamp', 'ts'):
        if f in rec:
            v = rec[f]
            try:
                return datetime.fromisoformat(v).isoformat()
            except Exception:
                try:
                    return datetime.utcfromtimestamp(float(v)).isoformat()
                except Exception:
                    return str(v)
    return None


def process_record(rec, patterns):
    out = {}
    out['ts'] = normalize_ts(rec)
    # anonymize common ip fields
    for f in ('src_ip', 'src', 'client_ip', 'ip'):
        if f in rec:
            out[f] = anonymize_ip(rec[f])
    # hash user/account ids/emails
    for f in ('user', 'username', 'email', 'account'):
        if f in rec:
            out[f] = hash_value(str(rec[f]))
    # basic text
    text = None
    for f in ('message', 'msg', 'request', 'url', 'payload', 'body'):
        if f in rec and isinstance(rec[f], str):
            text = rec[f]
            break
    if not text:
        text = json.dumps(rec)
    out['is_saas'] = bool(detect_saas(text, patterns))
    # time features
    if out['ts']:
        try:
            dt = datetime.fromisoformat(out['ts'])
            out['hour'] = dt.hour
            out['dow'] = dt.weekday()
        except Exception:
            out['hour'] = None
            out['dow'] = None
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--in', '-i', dest='infile', required=True)
    p.add_argument('--out', '-o', default='data/cleaned.jsonl')
    p.add_argument('--allowed', '-a', help='allowed_saas JSON')
    args = p.parse_args()

    allowed = None
    if args.allowed:
        allowed = load_allowed_saas(args.allowed)
    patterns = build_patterns(allowed)
    with open(args.infile, encoding='utf-8') as inh, open(args.out, 'w', encoding='utf-8') as outh:
        for line in inh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                # skip non-json lines
                continue
            out = process_record(rec, patterns)
            outh.write(json.dumps(out, ensure_ascii=False) + '\n')

    print('Wrote cleaned dataset to', args.out)


if __name__ == '__main__':
    main()
