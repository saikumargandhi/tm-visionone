from tm_visionone import VisionOneClient

API_KEY = "<YOUR_API_KEY>"

def test_list_objects_default():
    client = VisionOneClient(api_key=API_KEY, region="us")
    result = client.get_suspicious_objects(top=10)
    print("List result (default):", result)
    assert result["success"] is True
    assert "items" in result["data"]


def test_list_objects_with_filter():
    client = VisionOneClient(api_key=API_KEY, region="us")
    result = client.get_suspicious_objects(top=10, filter_expr="type eq 'url'")
    print("List result (with filter):", result)
    assert result["success"] is True
    assert "items" in result["data"]
