import requests
from tm_visionone import VisionOneClient

API_KEY = "<YOUR_API_KEY>"

def test_invalid_region():
    client = VisionOneClient(api_key=API_KEY, region="xx")
    result = client.healthcheck()
    print("Invalid region fallback result:", result)
    assert result["success"] in (True, False)
    assert "data" in result

def test_network_error(monkeypatch):
    client = VisionOneClient(api_key=API_KEY, region="us")

    def fake_request(*args, **kwargs):
        raise requests.RequestException("Simulated network error")

    monkeypatch.setattr("requests.request", fake_request)
    result = client.healthcheck()
    print("Simulated error result:", result)
    assert result["success"] is False
    assert result["error"]["code"] == "unavailable"
    assert "Simulated network error" in result["error"]["message"]
