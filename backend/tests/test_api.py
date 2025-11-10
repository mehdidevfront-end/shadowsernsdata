from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_assets():
    response = client.get("/assets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_risks():
    response = client.get("/risks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_graph_asset():
    response = client.get("/graph/test-asset")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data

def test_compliance_kpis():
    response = client.get("/compliance")
    assert response.status_code == 200
    data = response.json()
    assert "total_assets" in data
    assert "total_risks" in data
    assert "high_risks" in data
    assert "rgpd_coverage" in data

def test_finops_kpis():
    response = client.get("/finops")
    assert response.status_code == 200
    data = response.json()
    assert "monthly_cloud_cost" in data
    assert "orphaned_assets_count" in data
    assert "top_cost_services" in data