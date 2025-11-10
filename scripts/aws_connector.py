#!/usr/bin/env python3
"""AWS connector script: list EC2, S3 buckets and IAM users and output standardized JSON.

Requires AWS credentials in environment (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY) or configured profile.
"""
import boto3
import json
from datetime import datetime


def list_ec2():
    ec2 = boto3.client('ec2')
    resp = ec2.describe_instances()
    instances = []
    for r in resp.get('Reservations', []):
        for i in r.get('Instances', []):
            instances.append({
                'id': i.get('InstanceId'),
                'type': 'ec2',
                'instance_type': i.get('InstanceType'),
                'region': ec2.meta.region_name,
                'state': i.get('State', {}).get('Name'),
                'tags': {t['Key']: t['Value'] for t in i.get('Tags', [])} if i.get('Tags') else {},
            })
    return instances


def list_s3():
    s3 = boto3.client('s3')
    resp = s3.list_buckets()
    buckets = []
    for b in resp.get('Buckets', []):
        buckets.append({'id': b['Name'], 'type': 's3', 'creation_date': b['CreationDate'].isoformat()})
    return buckets


def list_iam():
    iam = boto3.client('iam')
    resp = iam.list_users()
    users = []
    for u in resp.get('Users', []):
        users.append({'id': u['UserName'], 'type': 'iam_user', 'arn': u['Arn'], 'created': u['CreateDate'].isoformat()})
    return users


def main():
    out = {
        'collected_at': datetime.utcnow().isoformat() + 'Z',
        'resources': []
    }
    try:
        out['resources'].extend(list_ec2())
    except Exception as e:
        out['ec2_error'] = str(e)
    try:
        out['resources'].extend(list_s3())
    except Exception as e:
        out['s3_error'] = str(e)
    try:
        out['resources'].extend(list_iam())
    except Exception as e:
        out['iam_error'] = str(e)

    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
