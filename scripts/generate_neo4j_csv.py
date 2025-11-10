#!/usr/bin/env python3
"""Generate a CSV file suitable for `neo4j/import_dependencies.cypher` from a JSON list.

Input JSON format (example):
[
  {
    "from": {"id":"service-a","label":"Service","props": {"name":"A","type":"service"}},
    "to": {"id":"service-b","label":"Service","props": {"name":"B","type":"service"}},
    "rel": {"type":"DEPENDS_ON","props": {"weight":1}}
  }
]

Output: writes `dependencies.csv` in current dir with headers: from_id,from_label,from_props_json,to_id,to_label,to_props_json,rel_type,rel_props_json
"""
import argparse
import json
import csv


def generate(infile, outfile='dependencies.csv'):
    data = json.load(open(infile, 'r', encoding='utf-8'))
    with open(outfile, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['from_id','from_label','from_props_json','to_id','to_label','to_props_json','rel_type','rel_props_json'])
        for item in data:
            fr = item.get('from', {})
            to = item.get('to', {})
            rel = item.get('rel', {})
            w.writerow([
                fr.get('id',''),
                fr.get('label','Service'),
                json.dumps(fr.get('props', {}), ensure_ascii=False),
                to.get('id',''),
                to.get('label','Service'),
                json.dumps(to.get('props', {}), ensure_ascii=False),
                rel.get('type','DEPENDS_ON'),
                json.dumps(rel.get('props', {}), ensure_ascii=False),
            ])
    print('Wrote', outfile)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--infile', required=True)
    p.add_argument('--outfile', default='dependencies.csv')
    args = p.parse_args()
    generate(args.infile, args.outfile)
