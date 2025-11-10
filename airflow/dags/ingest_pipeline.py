from __future__ import annotations
import json
import time
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from kafka import KafkaProducer, KafkaConsumer
from minio import Minio

DEFAULT_ARGS = {
    'owner': 'airflow',
    'retries': 1,
}

dag = DAG(
    dag_id='ingest_json_to_kafka_to_minio',
    default_args=DEFAULT_ARGS,
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
)

KAFKA_BOOTSTRAP = 'kafka:9092'
KAFKA_TOPIC = 'assets_raw'
MINIO_ENDPOINT = 'minio:9000'
MINIO_ACCESS = 'minioadmin'
MINIO_SECRET = 'minioadmin'
MINIO_BUCKET = 'assets_raw'


def produce_sample(**context):
    # Read sample JSON and publish to Kafka
    with open('/opt/airflow/dags/sample.json', 'r') as f:
        data = json.load(f)

    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BOOTSTRAP],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )
    producer.send(KAFKA_TOPIC, data)
    producer.flush()
    producer.close()
    return 'produced'


def consume_and_store(**context):
    # Consume messages and write to MinIO
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BOOTSTRAP],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=5000,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )

    client = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS, secret_key=MINIO_SECRET, secure=False)
    # create bucket if not exists
    try:
        if not client.bucket_exists(MINIO_BUCKET):
            client.make_bucket(MINIO_BUCKET)
    except Exception:
        # ignore errors for idempotency
        pass

    stored = 0
    for msg in consumer:
        value = msg.value
        key = f"asset-{int(time.time()*1000)}.json"
        client.put_object(MINIO_BUCKET, key, data=json.dumps(value).encode('utf-8'), length=len(json.dumps(value).encode('utf-8')))
        stored += 1

    consumer.close()
    return f'stored={stored}'


produce = PythonOperator(task_id='produce_sample', python_callable=produce_sample, dag=dag)
consume = PythonOperator(task_id='consume_and_store', python_callable=consume_and_store, dag=dag)

produce >> consume
