"""
tm-visionone
------------

Python SDK for Trend Micro Vision One APIs.

Currently supports:
- Suspicious Object upload
- Suspicious Object listing
- Healthcheck (API connectivity)
"""

from .client import VisionOneClient

__all__ = ["VisionOneClient"]
__version__ = "0.1.0"
