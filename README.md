# tm-visionone

[![PyPI version](https://img.shields.io/pypi/v/tm-visionone.svg)](https://pypi.org/project/tm-visionone/)
[![Python versions](https://img.shields.io/pypi/pyversions/tm-visionone.svg)](https://pypi.org/project/tm-visionone/)
[![License](https://img.shields.io/github/license/saikumargandhi/tm-visionone.svg)](LICENSE)

A lightweight Python SDK for **Trend Micro Vision One** (Suspicious Objects API v3).  
Easily upload, list, and manage suspicious objects (IOCs) using simple Python code.

---

## 🚀 Features

- Upload multiple IOCs (URLs, IPs, Domains, Hashes, Emails) in one call
- List suspicious objects with filters & ordering
- Manual pagination support (`get_next_page`)
- Healthcheck API to validate connectivity
- Handles 429 rate limits with `Retry-After` headers
- Region-aware (`us`, `eu`, `jp`, `sg`, `au`, `in`)
- Optional logging

---

## 📦 Installation

```bash
pip install tm-visionone
```

---

## ⚡ Quick Usage

```python
from tm_visionone import VisionOneClient

# Initialize client
client = VisionOneClient(api_key="YOUR_API_KEY", region="us")

# Healthcheck
print(client.healthcheck())

# Upload IOCs
objects = [
    {"url": "http://badsite.com", "description": "Malicious test site", "scanAction": "block"},
    {"ip": "45.77.23.11", "description": "Suspicious IP", "scanAction": "log"},
]
print(client.upload_suspicious_objects(objects))

# List suspicious objects (first page, up to 50 items)
result = client.get_suspicious_objects(top=50)
print(result["items"])
```

---

## 🔧 Advanced Usage

### Filtering & Ordering

```python
# List only high-risk URLs
result = client.get_suspicious_objects(
    filter_expr="type eq 'url' AND riskLevel eq 'high'",
    order_by="lastModifiedDateTime desc",
    top=50
)
for item in result.get("items", []):
    print(item)
```

### Pagination

```python
# Get first page
result = client.get_suspicious_objects(top=50)
all_items = result.get("items", [])

# Fetch next pages manually
while "nextLink" in result:
    result = client.get_next_page(result["nextLink"])
    all_items.extend(result.get("items", []))

print(f"Total IOCs collected: {len(all_items)}")
```

---

## 🧪 Testing

Clone the repo and run the test suite:

```bash
git clone https://github.com/saikumargandhi/tm-visionone.git
cd tm-visionone
pip install -r requirements-dev.txt
pytest -s tests/
```

---

## 📜 License

MIT © 2025 Sai Kumar Gandhi

---

## 🙏 Attribution

If you use `tm-visionone` in your project, please retain the following notice:

```
Copyright (c) 2025 Sai Kumar Gandhi
Licensed under the MIT License (see LICENSE file).
```