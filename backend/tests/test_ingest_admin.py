from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ingest_and_list():
    batch = [
        {
            "ip": "10.0.0.99",
            "mac": "AA:BB:CC:DD:EE:FF",
            "domain": "drive.google.com",
            "hostname": "laptop-test",
        }
    ]
    r = client.post("/api/ingest/events", json=batch)
    assert r.status_code == 200
    data = r.json()
    assert data["stored"] >= 1

    # assets should contain at least one device
    r2 = client.get("/api/assets/")
    assert r2.status_code == 200
    assets = r2.json()
    assert isinstance(assets, list)
    assert len(assets) >= 1

    # services should be available
    r3 = client.get("/api/services/")
    assert r3.status_code == 200
    services = r3.json()
    assert isinstance(services, list)
    assert len(services) >= 1

    # approve first service
    sid = services[0]["id"]
    r4 = client.post(f"/api/services/{sid}/approve")
    assert r4.status_code == 200
    assert r4.json()["approved"] is True
