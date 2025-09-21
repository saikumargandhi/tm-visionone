from tm_visionone import VisionOneClient

API_KEY = "api_key_here"

def test_list_default():
    client = VisionOneClient(api_key=API_KEY, region="us")
    result = client.get_suspicious_objects()
    assert isinstance(result, dict)
    print("List result (default):", result)

def test_list_with_filter():
    client = VisionOneClient(api_key=API_KEY, region="us")
    result = client.get_suspicious_objects(
        filter_expr="type eq 'url' AND riskLevel eq 'high'",
        top=50,
        order_by="lastModifiedDateTime desc"
    )
    assert isinstance(result, dict)
    print("List result (with filter):", result)