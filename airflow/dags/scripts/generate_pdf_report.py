#!/usr/bin/env python3
"""Generate a weekly PDF report from assets and risks and save to reports/.

Saves file to reports/weekly_report_<date>.pdf
If MINIO env vars present, uploads to MinIO.
"""
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

try:
    from minio import Minio
except Exception:
    Minio = None

from ...backend.app.storage import list_assets, list_risks


def create_pdf(path):
    assets = list_assets()
    risks = list_risks()
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont('Helvetica-Bold', 16)
    c.drawString(72, 750, 'Weekly Security Report')
    c.setFont('Helvetica', 10)
    c.drawString(72, 730, f'Date: {datetime.utcnow().isoformat()}')

    c.drawString(72, 700, f'Total assets: {len(assets)}')
    c.drawString(72, 685, f'Total risks: {len(risks)}')

    c.drawString(72, 650, 'Top risks:')
    y = 635
    for r in risks[:20]:
        c.drawString(80, y, f"- {r.get('id')} [{r.get('severity')}] {r.get('title')}")
        y -= 12
        if y < 72:
            c.showPage()
            y = 750

    c.showPage()
    c.save()


def upload_minio(path, bucket='reports'):
    if Minio is None:
        print('minio library not installed; skipping upload')
        return
    endpoint = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
    access = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
    secret = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
    client = Minio(endpoint, access_key=access, secret_key=secret, secure=False)
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
    object_name = os.path.basename(path)
    client.fput_object(bucket, object_name, path)
    print('Uploaded', object_name, 'to', bucket)


def main():
    os.makedirs('reports', exist_ok=True)
    fname = f'reports/weekly_report_{datetime.utcnow().date().isoformat()}.pdf'
    create_pdf(fname)
    print('Wrote', fname)
    # optional upload
    upload_minio(fname)


if __name__ == '__main__':
    main()
