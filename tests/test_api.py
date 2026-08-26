from fastapi.testclient import TestClient

from tsnt.api.app import create_app


def test_health_and_snii_endpoint():
    client = TestClient(create_app())
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    response = client.post(
        "/v1/scoring/snii",
        json={
            "components": {
                "centrality": 10,
                "throughput": 8,
                "control": 6,
                "cascade": 4,
                "substitutability": 2,
            }
        },
    )
    assert response.status_code == 200
    assert response.json()["published"] == "6.70"
