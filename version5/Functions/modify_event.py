import requests
import logging
import json
import sys
import os
from dotenv import load_dotenv

# Add the parent directory to sys.path to import logger_utility
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logger_utility import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger()

# Function to modify an existing event
def modify_event(event_id, event_data):
    try:
        # Fetch access token directly from environment variables
        access_token = os.getenv("ACCESS_TOKEN")  # Fetch access token from .env file
        if not access_token:
            raise ValueError("Access token not found in environment variables.")

        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Construct URL to modify event using Microsoft Graph API
        url = f'https://graph.microsoft.com/v1.0/me/events/{event_id}'
        
        # Make PATCH request to update the event
        response = requests.patch(url, json=event_data, headers=headers)

        # Handle the response status
        if response.status_code == 200:
            logger.info(f'Event {event_id} modified successfully.')
        else:
            error_message = f'Failed to modify event {event_id}: {response.json()}'
            logger.error(error_message)
            raise Exception(error_message)

    except requests.exceptions.RequestException as e:
        # Handle issues related to the network or API request
        logger.error(f"RequestException: {str(e)}")
    except Exception as e:
        logger.error(f"Error modifying event: {str(e)}")

# Example usage
if __name__ == "__main__":
    event_id_to_modify = "event_id_here"  # Replace with actual event ID

    try:
        # Read the event modification data from a JSON file
        with open('modify_existing_event.json') as json_file:
            event_data_to_modify = json.load(json_file)

        # Call modify_event to update the event
        modify_event(event_id_to_modify, event_data_to_modify)

    except FileNotFoundError as e:
        # Handle file not found error for the JSON file
        logger.error(f"File not found: {str(e)}")
    except json.JSONDecodeError as e:
        # Handle invalid JSON format error
        logger.error(f"JSONDecodeError: {str(e)}")
    except Exception as e:
        # Handle other exceptions
        logger.error(f"Error loading event data or modifying event: {str(e)}")
