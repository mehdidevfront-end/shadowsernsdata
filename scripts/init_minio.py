#!/usr/bin/env python3
"""Initialise les buckets MinIO et place un fichier test.

Usage:
  python scripts/init_minio.py --endpoint minio:9000 --access minioadmin --secret minioadmin
"""
import argparse
from minio import Minio
from minio.error import S3Error


def main(endpoint, access, secret, bucket_names):
    client = Minio(endpoint, access_key=access, secret_key=secret, secure=False)
    for b in bucket_names:
        try:
            if not client.bucket_exists(b):
                print(f"Creating bucket: {b}")
                client.make_bucket(b)
            else:
                print(f"Bucket already exists: {b}")
        except S3Error as e:
            print(f"Error creating bucket {b}: {e}")

    # upload a small test file
    test_obj = b'{"ok": true, "ts": "2025-11-07T00:00:00Z"}'
    client.put_object(bucket_names[0], 'init.json', data=bytes(test_obj), length=len(test_obj), content_type='application/json')
    print("Uploaded test object to", bucket_names[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', default='localhost:9000')
    parser.add_argument('--access', default='minioadmin')
    parser.add_argument('--secret', default='minioadmin')
    parser.add_argument('--buckets', default='assets_raw,assets_curated')
    args = parser.parse_args()
    buckets = [b.strip() for b in args.buckets.split(',') if b.strip()]
    main(args.endpoint, args.access, args.secret, buckets)
