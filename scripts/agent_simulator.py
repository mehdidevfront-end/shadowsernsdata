#!/usr/bin/env python3
"""Agent simulator: envoie périodiquement des événements de découverte au backend.
Utilisation:
  python scripts/agent_simulator.py --url http://localhost:8000 --interval 5
"""
import argparse
import random
import time
import requests
from datetime import datetime, timezone

SERVICES = [
    ("drive.google.com", "Google Drive"),
    ("dropbox.com", "Dropbox"),
    ("intranet.local", "Intranet"),
    ("slack.com", "Slack"),
]

HOSTNAMES = ["laptop-alice", "laptop-bob", "srv-logs", "wifi-ap-01"]

MACS = [
    "AA:BB:CC:DD:EE:01",
    "AA:BB:CC:DD:EE:02",
    "AA:BB:CC:DD:EE:03",
    "AA:BB:CC:DD:EE:04",
]

IPS = [
    "10.0.0.10",
    "10.0.0.11",
    "10.0.0.12",
    "10.0.0.13",
    "10.0.0.20",
]


def generate_event():
    domain, _ = random.choice(SERVICES)
    return {
        "ip": random.choice(IPS),
        "mac": random.choice(MACS),
        "domain": domain,
        "hostname": random.choice(HOSTNAMES),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL du backend")
    parser.add_argument("--interval", type=int, default=5, help="Intervalle en secondes entre envois")
    args = parser.parse_args()

    ingest_endpoint = args.url.rstrip('/') + "/api/ingest/events"
    print(f"Envoi des événements vers {ingest_endpoint} toutes les {args.interval}s")
    while True:
        batch = [generate_event() for _ in range(random.randint(1, 3))]
        try:
            r = requests.post(ingest_endpoint, json=batch, timeout=10)
            if r.status_code == 200:
                print(f"OK stored={r.json().get('stored')} received={r.json().get('received')}")
            else:
                print(f"Erreur {r.status_code}: {r.text}")
        except Exception as e:
            print(f"Exception: {e}")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
