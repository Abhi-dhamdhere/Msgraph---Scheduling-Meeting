import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("api_logger")


class APIError(Exception):
    """
    Custom Exception for handling API errors.
    """
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


def make_request(
    url: str,
    method: str,
    headers: Dict[str, str],
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 10
) -> Dict[str, Any]:
    """
    Generic function to make HTTP requests.
    Improved to handle additional scenarios.
    """
    try:
        logger.info(f"Making {method} request to {url} with payload: {payload}")
        response = requests.request(method, url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise APIError(
                f"Unexpected response: {response.status_code} - {response.text}",
                response.status_code
            )
    except requests.Timeout:
        logger.error(f"Request to {url} timed out.")
        raise APIError(f"Request timed out: {url}")
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error during request to {url}: {http_err}")
        raise APIError(f"HTTP error: {http_err}", status_code=response.status_code)
    except requests.RequestException as req_err:
        logger.error(f"General request error to {url}: {req_err}")
        raise APIError(f"Request failed: {req_err}")
    except Exception as ex:
        logger.error(f"Unexpected error during request to {url}: {ex}")
        raise APIError(f"Unexpected error: {ex}")
