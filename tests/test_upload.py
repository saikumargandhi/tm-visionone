from tm_visionone import VisionOneClient

API_KEY = "api_key_here"

def test_upload_suspicious_objects():
    client = VisionOneClient(api_key=API_KEY, region="us")
    objects = [
        {"url": "http://badsite.com", "description": "Testing script Malicious site", "scanAction": "block"},
        {"ip": "45.77.23.11", "description": "Testing Script Suspicious IP", "scanAction": "log"}
    ]
    result = client.upload_suspicious_objects(objects)
    # Vision One may return a list of dicts or a dict depending on input
    assert isinstance(result, (dict, list))
    print("Upload result:", result)

def test_upload_empty_list():
    client = VisionOneClient(api_key=API_KEY, region="us")
    result = client.upload_suspicious_objects([])
    assert "error" in result
    print("Upload empty result:", result)