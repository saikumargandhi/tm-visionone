from tm_visionone import VisionOneClient

API_KEY = "api_key_here"

def test_pagination():
    client = VisionOneClient(api_key=API_KEY, region="us")

    # Fetch first page
    result = client.get_suspicious_objects(top=50)
    assert isinstance(result, dict)
    assert "items" in result
    print("First page count:", len(result["items"]))

    # If there is a nextLink, fetch next page
    if "nextLink" in result:
        next_page = client.get_next_page(result["nextLink"])
        assert isinstance(next_page, dict)
        assert "items" in next_page
        print("Next page count:", len(next_page["items"]))
    else:
        print("No pagination available, single page only.")
