#!/usr/bin/env python3
"""Kafka producer script that publishes JSON messages to topic `assets_raw`.

Requirements:
  pip install kafka-python prometheus-client

Features:
 - Reads a JSON file or directory of JSON files and publishes each as a message
 - Emits Prometheus metrics on /metrics
 - Logs progress
"""
import argparse
import json
import logging
import os
from kafka import KafkaProducer
from prometheus_client import Counter, start_http_server

LOGGER = logging.getLogger('kafka_producer')
MSG_COUNTER = Counter('kafka_messages_published_total', 'Total messages published to Kafka')


def iter_json_files(path):
    if os.path.isdir(path):
        for fn in os.listdir(path):
            if fn.endswith('.json'):
                yield os.path.join(path, fn)
    else:
        yield path


def publish(bootstrap, topic, path):
    producer = KafkaProducer(bootstrap_servers=[bootstrap], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    total = 0
    for p in iter_json_files(path):
        with open(p, 'r', encoding='utf-8') as f:
            payload = json.load(f)
        key = None
        try:
            producer.send(topic, payload)
            producer.flush()
            total += 1
            MSG_COUNTER.inc()
            LOGGER.info('Published %s to %s', p, topic)
        except Exception as e:
            LOGGER.exception('Failed to publish %s: %s', p, e)
    producer.close()
    return total


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootstrap', default='kafka:9092')
    parser.add_argument('--topic', default='assets_raw')
    parser.add_argument('--path', required=True, help='JSON file or directory')
    parser.add_argument('--metrics-port', type=int, default=8001)
    args = parser.parse_args()

    start_http_server(args.metrics_port)
    LOGGER.info('Starting metrics server on %s', args.metrics_port)
    count = publish(args.bootstrap, args.topic, args.path)
    LOGGER.info('Published total messages: %d', count)


if __name__ == '__main__':
    main()
