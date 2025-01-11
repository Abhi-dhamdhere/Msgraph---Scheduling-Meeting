import requests
import logging
from functions.api.api_utility import APIError

logger = logging.getLogger("auth_logger")


class AuthenticationError(Exception):
    """
    Custom Exception for authentication-related errors.
    """
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


def get_access_token(client_id: str, client_secret: str, tenant_id: str, scope: str = "https://graph.microsoft.com/.default") -> str:
    """
    Retrieves an OAuth access token.
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
        "grant_type": "client_credentials"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        logger.info(f"Requesting access token for tenant: {tenant_id}")
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token", "")
    except requests.Timeout:
        logger.error("Request for access token timed out.")
        raise AuthenticationError("Request for access token timed out.")
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error during token request: {http_err}")
        raise AuthenticationError(f"HTTP error: {http_err}", response.status_code)
    except requests.RequestException as req_err:
        logger.error(f"Request failed during token retrieval: {req_err}")
        raise AuthenticationError(f"Request failed: {req_err}")
    except Exception as ex:
        logger.error(f"Unexpected error during token retrieval: {ex}")
        raise AuthenticationError(f"Unexpected error: {ex}")
