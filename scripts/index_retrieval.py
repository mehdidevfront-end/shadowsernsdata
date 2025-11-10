#!/usr/bin/env python3
"""Index text contexts into OpenSearch for retrieval.

Usage:
  python scripts/index_retrieval.py --input contexts.jsonl --index llm_contexts

Requires OPENSEARCH_URL env or default http://localhost:9200
"""
import argparse
import json
import os
from opensearchpy import OpenSearch, RequestsHttpConnection


def get_client():
    url = os.getenv('OPENSEARCH_URL', 'http://localhost:9200')
    # basic client
    return OpenSearch([url], connection_class=RequestsHttpConnection)


DEFAULT_MAPPING = {
    'mappings': {
        'properties': {
            'title': {'type': 'text'},
            'content': {'type': 'text'},
            'source': {'type': 'keyword'},
            'timestamp': {'type': 'date', 'format': 'strict_date_optional_time||epoch_millis'}
        }
    }
}


def index_file(client, idx, infile):
    if not client.indices.exists(idx):
        client.indices.create(idx, body=DEFAULT_MAPPING)
    cnt = 0
    with open(infile, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            doc = {
                'title': rec.get('title') or rec.get('id') or None,
                'content': rec.get('content') or rec.get('text') or rec.get('body') or json.dumps(rec),
                'source': rec.get('source') or 'ingest',
                'timestamp': rec.get('timestamp')
            }
            client.index(idx, body=doc)
            cnt += 1
    print('Indexed', cnt, 'docs to', idx)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', '-i', required=True, help='JSONL input with content')
    p.add_argument('--index', default='llm_contexts')
    args = p.parse_args()
    client = get_client()
    index_file(client, args.index, args.input)


if __name__ == '__main__':
    main()
