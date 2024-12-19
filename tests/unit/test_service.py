from fastapi.testclient import TestClient
from app.main import app

# Create a test client for the FastAPI app
client = TestClient(app)


def test_search_endpoint_no_filters():
    response = client.post("/api/search", json={"query": "red wine", "limit": 10})
    assert response.status_code == 200
    assert "results" in response.json()


def test_search_endpoint_with_filters():
    response = client.post(
        "/api/search",
        json={
            "query": "red wine",
            "limit": 5,
            "include": {"variety": "Red Wine", "rating": {"gte": 80}},
        },
    )
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) <= 5  # Ensure the limit is respected
    for result in results:
        assert result["metadata"]["rating"] >= 80  # Check the filter


def test_search_endpoint_invalid_request():
    response = client.post(
        "/api/search",
        json={
            "query": "red wine",
            "limit": 5,
            "include": {"rating": {"gte": 120}},  # Invalid rating range
        },
    )
    assert response.status_code == 422  # Validation should fail
