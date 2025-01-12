import sys
import os
from dotenv import load_dotenv
import requests
import logging

# Add the parent directory to sys.path to import logger_utility
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logger_utility import setup_logger

# Setup logging
logger = setup_logger()

# Load environment variables
load_dotenv()

# Retrieve the access token from the .env file
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise ValueError("Access token not found in environment variables.")

# Function to cancel an event
def cancel_event(event_id):
    try:
        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
        url = f'https://graph.microsoft.com/v1.0/me/events/{event_id}/cancel'
        
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            logger.info(f'Event {event_id} cancelled successfully.')
        else:
            logger.error(f'Failed to cancel event {event_id}: {response.json()}')

    except requests.exceptions.RequestException as e:
        logger.error(f"RequestException: {str(e)}")
    except Exception as e:
        logger.error(f"Error cancelling event: {str(e)}")

# Example usage
event_id_to_cancel = "event_id_here"  # Replace with actual event ID
cancel_event(event_id_to_cancel)
