from tm_visionone import VisionOneClient

API_KEY = "<YOUR_API_KEY>"

def test_upload_objects():
    client = VisionOneClient(api_key=API_KEY, region="us")
    objects = [
        {"url": "http://badsite.com/", "type": "url",
            "description": "Testing script Malicious site", "scanAction": "block"},
        {"ip": "45.77.23.11", "type": "ip",
            "description": "Testing Script Suspicious IP", "scanAction": "log"},
    ]
    result = client.upload_suspicious_objects(objects)
    print("Upload result:", result)
    assert result["success"] is True
    assert isinstance(result["data"], list)


def test_upload_empty():
    client = VisionOneClient(api_key=API_KEY, region="us")
    result = client.upload_suspicious_objects([])
    print("Upload empty result:", result)
    assert result["success"] is False
    assert result["error"]["code"] == "invalid_input"
