from tm_visionone import VisionOneClient

API_KEY = "<YOUR_API_KEY>"

def test_healthcheck_success():
    client = VisionOneClient(api_key=API_KEY, region="us")
    result = client.healthcheck()
    assert result["success"] is True
    assert result["data"]["connectivity"] is True
    assert result["data"]["status"] == "available"


def test_healthcheck_invalid_key():
    client = VisionOneClient(api_key="FAKEKEY", region="us")
    result = client.healthcheck()
    assert result["success"] is False
    assert result["error"] is not None
    assert "invalid" in result["error"]["message"].lower()
