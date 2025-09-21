# tm-visionone

A Python client for the [Trend Micro Vision One API v3](https://automation.trendmicro.com/xdr/api-v3/).

This package helps you integrate with Trend Micro Vision One (XDR) services — especially **Suspicious Object List** and **Connectivity health check** APIs — with clean, consistent responses and retry handling.

---

## ✨ Features
- Upload suspicious objects (IOCs: URL, IP, domain, file hashes, email).
- List suspicious objects with filters, ordering, and pagination support.
- Get next page of results using `nextLink`.
- Health check API for connectivity & token validation.
- Handles **rate limiting (429)** and transient errors (**500, 502, 503, 504**) with retries.
- Region-aware (`us`, `eu`, `jp`, `sg`, `au`, `in`).
- Optional logging.

---

## 📦 Installation

### From PyPI (after release):
```bash
pip install tm-visionone
```

### From TestPyPI (for testing):
```bash
pip install -i https://test.pypi.org/simple/ tm-visionone
```

---

## 🚀 Quick Usage

```python
from tm_visionone import VisionOneClient

API_KEY = "YOUR_API_KEY"

client = VisionOneClient(api_key=API_KEY, region="us", enable_logging=True)

# Healthcheck
print(client.healthcheck())
# -> {'success': True, 'data': {'connectivity': True, 'status': 'available', 'message': 'API reachable and token valid'}, 'error': None}

# Upload suspicious objects
objects = [
    {"url": "http://malicious.example", "description": "Test URL", "scanAction": "log", "riskLevel": "high"}
]
print(client.upload_suspicious_objects(objects))
# -> {'success': True, 'data': [{'status': 201}], 'error': None}

# List suspicious objects
result = client.get_suspicious_objects(top=10)
print(result["data"]["items"])  # Paginated results
```

---

## 📖 Advanced Usage

### Pagination
```python
result = client.get_suspicious_objects(top=10)
print(result["data"]["items"])

if "nextLink" in result["data"]:
    next_page = client.get_next_page(result["data"]["nextLink"])
    print(next_page["data"]["items"])
```

### Logging
Enable built-in logging:
```python
client = VisionOneClient(api_key=API_KEY, region="us", enable_logging=True)
```

---

## 🧪 Running Tests

Clone the repo and install dev dependencies:
```bash
git clone https://github.com/saikumargandhi/tm-visionone.git
cd tm-visionone
pip install -r requirements-dev.txt
pytest -s tests/
```

---

## ⚖️ License

This project is licensed under the MIT License.

---

## 🙏 Attribution

- Built by [Sai Kumar Gandhi](https://github.com/saikumargandhi)
- Powered by [Trend Micro Vision One APIs](https://automation.trendmicro.com/xdr/api-v3/)
