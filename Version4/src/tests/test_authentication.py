import unittest
from unittest.mock import patch, MagicMock
from authentication_utility import AuthenticationConfig, AuthenticationUtility


class TestAuthenticationUtility(unittest.TestCase):
    @patch("msal.PublicClientApplication.initiate_device_flow")
    @patch("msal.PublicClientApplication.acquire_token_by_device_flow")
    def test_get_access_token_success(self, mock_acquire_token, mock_initiate_device_flow):
        # Mock the MSAL device flow
        mock_initiate_device_flow.return_value = {"user_code": "1234", "verification_uri": "http://example.com"}
        mock_acquire_token.return_value = {"access_token": "mock_access_token"}

        # Set up the authentication config
        config = AuthenticationConfig(client_id="mock_client_id", tenant_id="mock_tenant_id", scopes=["mock_scope"])
        auth_util = AuthenticationUtility(config)

        # Test get_access_token
        access_token = auth_util.get_access_token()

        self.assertEqual(access_token, "mock_access_token")
        mock_initiate_device_flow.assert_called_once()
        mock_acquire_token.assert_called_once()

    @patch("msal.PublicClientApplication.initiate_device_flow")
    def test_get_access_token_failure(self, mock_initiate_device_flow):
        # Simulate failure to initiate the device flow
        mock_initiate_device_flow.side_effect = Exception("Failed to initiate device flow")

        config = AuthenticationConfig(client_id="mock_client_id", tenant_id="mock_tenant_id", scopes=["mock_scope"])
        auth_util = AuthenticationUtility(config)

        with self.assertRaises(RuntimeError) as context:
            auth_util.get_access_token()

        self.assertIn("Error obtaining access token", str(context.exception))


if __name__ == "__main__":
    unittest.main()
