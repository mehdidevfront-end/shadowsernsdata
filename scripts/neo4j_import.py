#!/usr/bin/env python3
"""Import dependencies into Neo4j from a JSON file containing nodes/relations.

Requirements:
  pip install neo4j

Input format (example):
[
  {"from": {"id":"service-a","label":"Service"}, "to": {"id":"service-b","label":"Service"}, "rel": {"type":"DEPENDS_ON","weight":1}}
]
"""
import argparse
import json
from neo4j import GraphDatabase


def upsert_node(tx, nid, label, props=None):
    props = props or {}
    props_clause = ', '.join([f'{k}: $_props.{k}' for k in props.keys()]) if props else ''
    # Use MERGE on id
    tx.run(f"MERGE (n:{label} {{id: $id}}) SET n += $props", id=nid, props=props)


def create_rel(tx, from_id, from_label, to_id, to_label, rel_type, rel_props=None):
    rel_props = rel_props or {}
    tx.run(
        f"MATCH (a:{from_label} {{id:$from_id}}), (b:{to_label} {{id:$to_id}}) MERGE (a)-[r:{rel_type}]->(b) SET r += $props",
        from_id=from_id, to_id=to_id, props=rel_props,
    )


def import_file(uri, user, password, infile):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    data = json.load(open(infile, 'r', encoding='utf-8'))
    with driver.session() as sess:
        for item in data:
            fr = item['from']
            to = item['to']
            rel = item.get('rel', {})
            props_from = fr.get('props', {})
            props_to = to.get('props', {})
            sess.write_transaction(upsert_node, fr['id'], fr.get('label', 'Service'), props_from)
            sess.write_transaction(upsert_node, to['id'], to.get('label', 'Service'), props_to)
            sess.write_transaction(create_rel, fr['id'], fr.get('label', 'Service'), to['id'], to.get('label', 'Service'), rel.get('type', 'DEPENDS_ON'), rel.get('props', {}))
    driver.close()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--uri', default='bolt://neo4j:7687')
    p.add_argument('--user', default='neo4j')
    p.add_argument('--password', default='')
    p.add_argument('--infile', required=True)
    args = p.parse_args()
    import_file(args.uri, args.user, args.password, args.infile)
