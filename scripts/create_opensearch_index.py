#!/usr/bin/env python3
"""Create OpenSearch index with mapping for assets."""
import argparse
import json
import requests


MAPPING = {
  "settings": {"number_of_shards": 1},
  "mappings": {
    "properties": {
      "id": {"type": "keyword"},
      "type": {"type": "keyword"},
      "criticite": {"type": "keyword"},
      "timestamp": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
      "payload": {"type": "object", "enabled": True}
    }
  }
}


def main(host='http://localhost:9200', index='assets'):
    url = f"{host.rstrip('/')}/{index}"
    r = requests.put(url, json=MAPPING)
    if r.status_code in (200,201):
        print(f"Index '{index}' created or already exists.")
    else:
        print("Failed to create index:", r.status_code, r.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='http://opensearch:9200')
    parser.add_argument('--index', default='assets')
    args = parser.parse_args()
    main(args.host, args.index)
