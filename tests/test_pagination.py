from tm_visionone import VisionOneClient

API_KEY = "<YOUR_API_KEY>"

def test_pagination():
    client = VisionOneClient(api_key=API_KEY, region="us")

    # First page
    result = client.get_suspicious_objects(top=5)
    assert result["success"] is True
    assert "items" in result["data"]

    next_link = result["data"].get("nextLink")
    if next_link:
        next_page = client.get_next_page(next_link)
        assert next_page["success"] is True
        assert "items" in next_page["data"]
