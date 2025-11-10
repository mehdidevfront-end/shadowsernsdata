FROM apache/airflow:2.7.1

# Install small set of extras for Kafka and MinIO access
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
