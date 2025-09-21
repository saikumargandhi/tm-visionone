from tm_visionone import VisionOneClient

# ⚠️ Replace with your real API key for testing
API_KEY = "api_key_here"

def test_healthcheck_success():
    client = VisionOneClient(api_key=API_KEY, region="us")
    result = client.healthcheck()
    assert "connectivity" in result
    assert isinstance(result["connectivity"], bool)
    print("Healthcheck result:", result)

def test_healthcheck_invalid_key():
    client = VisionOneClient(api_key="FAKEKEY", region="us")
    result = client.healthcheck()
    assert result["connectivity"] is False
    print("Invalid key result:", result)