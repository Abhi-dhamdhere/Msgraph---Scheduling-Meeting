from pydantic import BaseModel, ValidationError, Field
from typing import List
import os
import msal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AuthenticationConfig(BaseModel):
    """
    Configuration model for Azure AD authentication.
    """
    client_id: str = Field(..., description="Azure AD Application Client ID")
    tenant_id: str = Field(..., description="Azure AD Tenant ID")
    scopes: List[str] = Field(..., description="List of permissions required for Microsoft Graph API")

    @staticmethod
    def load_from_env():
        """
        Load authentication configuration from environment variables.
        """
        try:
            return AuthenticationConfig(
                client_id=os.getenv("CLIENT_ID"),
                tenant_id=os.getenv("TENANT_ID"),
                scopes=os.getenv("SCOPES", "").split(",")
            )
        except ValidationError as e:
            raise ValueError(f"Invalid configuration: {e}")

class AuthenticationUtility:
    """
    Utility for managing Azure AD authentication using MSAL.
    """
    def __init__(self, config: AuthenticationConfig):
        self.config = config
        self.authority: str = f"https://login.microsoftonline.com/{self.config.tenant_id}"
        self.app: msal.PublicClientApplication = msal.PublicClientApplication(
            self.config.client_id,
            authority=self.authority
        )

    def get_access_token(self) -> str:
        """
        Obtain an access token using MSAL.
        """
        flow = self.app.initiate_device_flow(scopes=self.config.scopes)
        if "user_code" in flow:
            print(f"Visit {flow['verification_uri']} and enter the code {flow['user_code']} to authenticate.")
            result = self.app.acquire_token_by_device_flow(flow)
            if "access_token" in result:
                return result["access_token"]
            else:
                raise Exception(f"Authentication failed: {result.get('error_description', 'Unknown error')}.")
        else:
            raise Exception("Failed to initiate device flow.")

# Main script
if __name__ == "__main__":
    try:
        # Load configuration from environment variables
        config = AuthenticationConfig.load_from_env()
        
        # Initialize the authentication utility
        auth_utility = AuthenticationUtility(config)
        
        # Get and print the access token
        access_token = auth_utility.get_access_token()
        print(f"Access Token: {access_token}")
    except Exception as e:
        print(f"An error occurred: {e}")
