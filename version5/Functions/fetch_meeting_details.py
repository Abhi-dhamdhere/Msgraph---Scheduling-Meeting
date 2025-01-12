from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Literal
import requests
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to sys.path to import logger_utility
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from logger_utility import setup_logger

# Initialize the logger
logger = setup_logger()

class FetchMeetingDetailsInput(BaseModel):
    access_token: Annotated[str, Field(description="The access token for authentication.")]
    event_id: Annotated[str, Field(description="The ID of the event to retrieve details for.")]
    auth_mode: Annotated[
        Literal["app", "me"],
        Field(description="Authentication mode. Possible values: 'app' or 'me'.")
    ]

    @model_validator(mode="after")
    def validate_inputs(cls, values):
        """
        Validate inputs to ensure they are not empty and have valid values.
        """
        logger.debug("Validating input fields...")

        # Validate access_token
        if not values.access_token.strip():
            error_message = "Invalid access_token: The token must not be empty."
            logger.error(error_message)
            raise ValueError(error_message)

        # Validate event_id
        if not values.event_id.strip():
            error_message = "Invalid event_id: Event ID must not be empty."
            logger.error(error_message)
            raise ValueError(error_message)

        # Validate auth_mode
        if values.auth_mode not in {"app", "me"}:
            error_message = f"Invalid auth_mode: '{values.auth_mode}'. Supported values are 'app' or 'me'."
            logger.error(error_message)
            raise ValueError(error_message)

        logger.debug("Input validation passed.")
        return values

class Organizer(BaseModel):
    name: str
    email: str

class EventDetails(BaseModel):
    id: str
    is_online_meeting: bool
    start_datetime: datetime
    end_datetime: datetime
    location_name: str
    organizer: Organizer
    join_url: str

def fetch_meeting_details(input: Annotated[FetchMeetingDetailsInput, "Input for fetching meeting details."]) -> EventDetails:
    """
    Fetch detailed information about a specific event using its event ID.

    Args:
        input (FetchMeetingDetailsInput): Input containing the access token, event ID, and auth mode.

    Returns:
        EventDetails: Detailed information about the event.

    Raises:
        Exception: If the API request fails.
    """
    try:
        logger.debug(f"Fetching meeting details for Event ID: {input.event_id} with auth_mode: {input.auth_mode}")

        # Determine the endpoint URL based on auth_mode
        if input.auth_mode == "me":
            url = f"https://graph.microsoft.com/v1.0/me/events/{input.event_id}"
        elif input.auth_mode == "app":
            url = f"https://graph.microsoft.com/v1.0/users/{input.event_id}"  # Adjust for specific app mode usage.
        else:
            raise ValueError("Invalid auth_mode. Supported values are 'app' and 'me'.")

        headers = {
            "Authorization": f"Bearer {input.access_token}",
            "Content-Type": "application/json",
        }

        logger.debug(f"Making GET request to URL: {url}")

        # Send the GET request
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            logger.info("Successfully fetched meeting details.")
            event = response.json()

            organizer = Organizer(
                name=event["organizer"]["emailAddress"]["name"],
                email=event["organizer"]["emailAddress"]["address"],
            )

            return EventDetails(
                id=event["id"],
                is_online_meeting=event.get("isOnlineMeeting", False),
                start_datetime=datetime.fromisoformat(event["start"]["dateTime"]),
                end_datetime=datetime.fromisoformat(event["end"]["dateTime"]),
                location_name=event.get("location", {}).get("displayName", "No location specified"),
                organizer=organizer,
                join_url=event.get("onlineMeeting", {}).get("joinUrl", "No online meeting URL"),
            )
        else:
            error_message = f"Error fetching meeting details: {response.status_code} - {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
    except Exception as e:
        logger.exception("An error occurred while fetching meeting details.")
        raise e

from dotenv import load_dotenv
# Test Main Method
if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    # Replace with your actual access token
    access_token = os.getenv("ACCESS_TOKEN")

    # Test input data
    input_data = FetchMeetingDetailsInput(
        access_token=access_token,
        event_id="AAMkADFlNDI3ZjFiLWRjODktNGY4OS05M2I4LWEzMWJlZTg4MTczNgBGAAAAAACiBko5nvE1TJgmNsnFk3xRBwD0NyRXjYGWS5J17R6mruzqAAAAAAENAAD0NyRXjYGWS5J17R6mruzqAAADA50wAAA=",  # Replace with a valid event ID
        auth_mode="me",  # Change to "app" if using app authentication
    )

    try:
        logger.debug("Starting the meeting details fetching process...")
        meeting_details = fetch_meeting_details(input_data)
        print("Fetched Meeting Details:\n")
        print(f"ID: {meeting_details.id}")
        print(f"Is Online Meeting: {meeting_details.is_online_meeting}")
        print(f"Start: {meeting_details.start_datetime}")
        print(f"End: {meeting_details.end_datetime}")
        print(f"Location: {meeting_details.location_name}")
        print(f"Organizer: {meeting_details.organizer.name} ({meeting_details.organizer.email})")
        print(f"Join URL: {meeting_details.join_url}")
    except Exception as e:
        logger.error(f"Error: {e}")