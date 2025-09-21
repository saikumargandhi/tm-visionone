import requests
from tm_visionone import VisionOneClient

API_KEY = "api_key_here"

def test_invalid_region():
    client = VisionOneClient(api_key=API_KEY, region="xx")
    result = client.healthcheck()
    assert "connectivity" in result
    print("Invalid region fallback result:", result)

def test_network_error(monkeypatch):
    client = VisionOneClient(api_key=API_KEY, region="us")

    def fake_request(*args, **kwargs):
        raise requests.RequestException("Simulated network error")

    monkeypatch.setattr("requests.request", fake_request)

    result = client.healthcheck()
    assert result["connectivity"] is False
    assert result["status"] == "unavailable"
    assert "Simulated network error" in result["message"]
    print("Simulated error result:", result)