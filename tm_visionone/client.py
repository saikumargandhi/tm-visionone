import requests
import time
import logging
from typing import List, Dict, Optional
from urllib.parse import urlparse

class VisionOneClient:
    """
    Python client for Trend Micro Vision One APIs (v3).

    Features:
    - Upload suspicious objects (bulk).
    - List suspicious objects (filters, ordering, time range).
    - API healthcheck.
    - Handles retries with "Retry-After" if present, or exponential backoff.
    - Optional logging.
    - Region-aware (us, eu, jp, sg, au, in).
    """

    REGION_MAP = {
        "us": "https://api.xdr.trendmicro.com",
        "eu": "https://api.eu.xdr.trendmicro.com",
        "jp": "https://api.xdr.trendmicro.co.jp",
        "sg": "https://api.sg.xdr.trendmicro.com",
        "au": "https://api.au.xdr.trendmicro.com",
        "in": "https://api.in.xdr.trendmicro.com",
    }

    def __init__(
        self,
        api_key: str,
        region: str = "us",
        enable_logging: bool = False,
        timeout: int = 30,
        max_retries: int = 5,
    ):
        # Base URL from region map unless explicitly overridden
        self.base_url = self.REGION_MAP.get(region, self.REGION_MAP["us"])
        self.api_key = api_key
        self.enable_logging = enable_logging
        self.timeout = timeout
        self.max_retries = max_retries

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Logger
        self.logger = logging.getLogger("tm-visionone")
        if enable_logging and not logging.getLogger().handlers:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s [%(levelname)s] %(message)s",
            )

    def _log(self, msg: str):
        if self.enable_logging:
            self.logger.info(msg)

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}{endpoint}"
        self._log(f"Request: {method} {url} | {kwargs}")

        # Ensure headers are always present
        if "headers" not in kwargs:
            kwargs["headers"] = self.headers

        for attempt in range(self.max_retries):
            try:
                resp = requests.request(method, url, timeout=self.timeout, **kwargs)

                # Handle rate-limiting (429 Too Many Requests)
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        wait_time = int(retry_after)
                        self._log(f"Rate limited. Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                    else:
                        wait_time = 2 ** attempt
                        self._log(f"Rate limited. Backoff {wait_time}s...")
                        time.sleep(wait_time)
                    continue

                resp.raise_for_status()

                if not resp.text.strip():
                    return {}

                data = resp.json()
                self._log(f"Response: {data}")
                return data

            except requests.HTTPError:
                self._log(f"HTTP error {resp.status_code}: {resp.text}")
                return {"connectivity": False, "error": resp.status_code, "message": resp.text}

            except requests.RequestException as e:
                self._log(f"Request failed: {e}")
                return {"connectivity": False, "error": "request_failed", "message": str(e)}

            except ValueError:
                self._log("Invalid JSON in response")
                return {"connectivity": False, "error": "invalid_json", "message": resp.text}

        return {"connectivity": False, "error": "max_retries_exceeded", "message": "Request failed after retries"}

    # === Suspicious Object APIs ===

    def upload_suspicious_objects(self, objects: List[Dict]) -> dict:
        """Upload multiple suspicious objects (IOCs)."""
        if not isinstance(objects, list) or not objects:
            return {"error": "invalid_input", "message": "objects must be a non-empty list"}
        return self._request("POST", "/v3.0/threatintel/suspiciousObjects", json=objects)

    def get_suspicious_objects(
        self,
        order_by: str = "lastModifiedDateTime desc",
        top: int = 100,
        start_datetime: Optional[str] = None,
        end_datetime: Optional[str] = None,
        filter_expr: Optional[str] = None,
    ) -> dict:
        """Retrieve suspicious objects (one page)."""
        params = {"orderBy": order_by, "top": top}
        if start_datetime:
            params["startDateTime"] = start_datetime
        if end_datetime:
            params["endDateTime"] = end_datetime

        headers = self.headers.copy()  # preserves Authorization
        if filter_expr:
            headers["TMV1-Filter"] = filter_expr

        return self._request(
            "GET", "/v3.0/threatintel/suspiciousObjects", params=params, headers=headers
        )

    # === Connectivity ===

    def healthcheck(self) -> dict:
        """
        Check API connectivity and token validity.

        Returns:
            {
                "connectivity": bool,
                "status": str,
                "message": str
            }
        """
        result = self._request("GET", "/v3.0/healthcheck/connectivity")

        if isinstance(result, dict) and result.get("status") == "available":
            return {
                "connectivity": True,
                "status": "available",
                "message": "API reachable and token valid",
            }

        return {
            "connectivity": False,
            "status": result.get("status", "unavailable") if isinstance(result, dict) else "unavailable",
            "message": result.get("message", "API unreachable or token invalid") if isinstance(result, dict) else "Unknown error",
        }
    
    # === Pagination ===

    def get_next_page(self, next_link: str) -> dict:
        """Retrieve next page of suspicious objects using nextLink from a previous response."""
        if not next_link:
            return {"error": "invalid_input", "message": "next_link must not be empty"}
        parsed = urlparse(next_link)
        # If absolute URL from API, use path+query
        endpoint = parsed.path + ("?" + parsed.query if parsed.query else "") if parsed.netloc else next_link
        return self._request("GET", endpoint)
