# Author: Abhishek Ravindra Dhamdhere
# Email: dhamdhereabhishek16@gmail.com
# Phone: 9594709185
# Organization: DisruptiveNext
# Supervisor: Mr. Prashant Mane

# Description: 
# This script is part of an internship task for developing an Attendance App. 
# It integrates with the Microsoft Graph API to interact with the user's calendar and fetch events. 
# Authentication is handled using MSAL (Microsoft Authentication Library) through the device code flow 
# to obtain an access token. 

# The script fetches calendar events and applies user-defined filters such as subject, start date, 
# and end date to identify relevant meetings. It displays key details of the filtered events, including:
# - Event ID
# - Subject
# - Start and end times
# - Location
# - Organizer details
# - Whether the event is an online meeting

# For online meetings, the script also retrieves the attendance report, including participant information, 
# if available. This functionality ensures the app provides accurate insights into meeting participation 
# and attendance.

# Trello Card Link: https://trello.com/c/q26wAMWs

import os
import logging
from typing import List, Dict, Union, Optional
from datetime import datetime

# Constants for HTTP methods and API URLs
GET_METHOD = "GET"
POST_METHOD = "POST"
API_BASE_URL = "https://api.schedulingplatform.com"

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_config_path(config_path: str) -> bool:
    """
    Validate the configuration file path.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    if not os.path.exists(config_path):
        logging.warning(f"Configuration file not found: {config_path}")
        return False
    return True

def fetch_events(api_key: str, filters: Optional[Dict[str, Union[str, int]]] = None) -> List[Dict[str, Union[str, datetime]]]:
    """
    Fetch a list of events from the scheduling API.

    Args:
        api_key (str): API key for authentication.
        filters (Optional[Dict[str, Union[str, int]]]): Filters to apply to the event query.

    Returns:
        List[Dict[str, Union[str, datetime]]]: List of events.
    """
    try:
        url = f"{API_BASE_URL}/events"
        headers = {"Authorization": f"Bearer {api_key}"}
        params = filters or {}

        # Simulate API request
        logging.info("Fetching events from API...")
        # response = requests.get(url, headers=headers, params=params)  # Uncomment when using requests library

        # Simulated response for demonstration purposes
        response = {"status_code": 200, "data": [{"id": 1, "title": "Meeting", "date": "2025-01-12T10:00:00"}]}  # Mock response
        if response["status_code"] != 200:
            raise ValueError(f"API returned error: {response['status_code']}")

        events = response["data"]
        for event in events:
            event["date"] = datetime.fromisoformat(event["date"])
        logging.info(f"Fetched {len(events)} events.")
        return events

    except ValueError as ve:
        logging.error(f"ValueError occurred: {ve}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return []

def fetch_events_in_date_range(api_key: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Union[str, datetime]]]:
    """
    Fetch events within a specific date range.

    Args:
        api_key (str): API key for authentication.
        start_date (datetime): Start of the date range.
        end_date (datetime): End of the date range.

    Returns:
        List[Dict[str, Union[str, datetime]]]: List of events within the date range.
    """
    filters = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
    return fetch_events(api_key, filters)

def schedule_meeting(api_key: str, meeting_details: Dict[str, Union[str, datetime]]) -> bool:
    """
    Schedule a new meeting using the scheduling API.

    Args:
        api_key (str): API key for authentication.
        meeting_details (Dict[str, Union[str, datetime]]): Details of the meeting to schedule.

    Returns:
        bool: True if the meeting was successfully scheduled, False otherwise.
    """
    try:
        url = f"{API_BASE_URL}/schedule"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = meeting_details

        # Simulate API request
        logging.info("Scheduling meeting...")
        # response = requests.post(url, headers=headers, json=payload)  # Uncomment when using requests library

        # Simulated response for demonstration purposes
        response = {"status_code": 201}  # Mock response
        if response["status_code"] != 201:
            raise ValueError(f"API returned error: {response['status_code']}")

        logging.info("Meeting scheduled successfully.")
        return True

    except ValueError as ve:
        logging.error(f"ValueError occurred: {ve}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False

def cancel_meeting(api_key: str, meeting_id: int) -> bool:
    """
    Cancel a scheduled meeting using the scheduling API.

    Args:
        api_key (str): API key for authentication.
        meeting_id (int): ID of the meeting to cancel.

    Returns:
        bool: True if the meeting was successfully canceled, False otherwise.
    """
    try:
        # Validate if meeting ID exists
        logging.info("Validating meeting ID before cancelation...")
        events = fetch_events(api_key)
        if not any(event["id"] == meeting_id for event in events):
            logging.warning(f"Meeting ID {meeting_id} does not exist.")
            return False

        url = f"{API_BASE_URL}/cancel/{meeting_id}"
        headers = {"Authorization": f"Bearer {api_key}"}

        # Simulate API request
        logging.info("Canceling meeting...")
        # response = requests.delete(url, headers=headers)  # Uncomment when using requests library

        # Simulated response for demonstration purposes
        response = {"status_code": 200}  # Mock response
        if response["status_code"] != 200:
            raise ValueError(f"API returned error: {response['status_code']}")

        logging.info("Meeting canceled successfully.")
        return True

    except ValueError as ve:
        logging.error(f"ValueError occurred: {ve}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False
