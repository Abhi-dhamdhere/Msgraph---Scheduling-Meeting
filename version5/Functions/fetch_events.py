from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Literal, Optional
import requests
import os
import sys
from datetime import datetime,timedelta
# Add the parent directory to sys.path to import logger_utility
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from logger_utility import setup_logger

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the logger
logger = setup_logger()

# Input Model for Fetching Events
class FetchEventsInput(BaseModel):
    access_token: Annotated[str, Field(description="The access token for authentication.")]
    auth_mode: Annotated[
        Literal["app", "me"],
        Field(description="Authentication mode. Possible values: 'app' or 'me'.")
    ]
    subject_filter: Optional[str] = Field(
        None, description="Filter for events by subject."
    )
    start_date: Optional[str] = Field(
        None, description="Start date for filtering events in ISO 8601 format (e.g., 2024-12-01T00:00:00Z)."
    )
    end_date: Optional[str] = Field(
        None, description="End date for filtering events in ISO 8601 format (e.g., 2024-12-31T23:59:59Z)."
    )

    @model_validator(mode="after")
    def validate_dates(cls, values):
        """
        Validate and ensure date strings are in ISO 8601 format with time and timezone.
        """
        logger.debug("Validating dates for event filtering...")
        if values.start_date:
            try:
                datetime.fromisoformat(values.start_date.replace("Z", "+00:00"))
            except ValueError:
                error_message = "Invalid start_date format. Expected ISO 8601 format (e.g., 2024-12-01T00:00:00Z)."
                logger.error(error_message)
                raise ValueError(error_message)

        if values.end_date:
            try:
                datetime.fromisoformat(values.end_date.replace("Z", "+00:00"))
            except ValueError:
                error_message = "Invalid end_date format. Expected ISO 8601 format (e.g., 2024-12-31T23:59:59Z)."
                logger.error(error_message)
                raise ValueError(error_message)

        logger.debug(f"Validated dates: start_date={values.start_date}, end_date={values.end_date}")
        return values

# Tool Function
def fetch_events(input: Annotated[FetchEventsInput, "Input for fetching calendar events."]) -> str:
    """
    Fetch events from the Microsoft Graph API with optional filters.

    Args:
        input (FetchEventsInput): Input containing access token, auth mode, and filters.

    Returns:
        str: JSON response of fetched events.

    Raises:
        Exception: If the API request fails.
    """
    try:
        logger.debug(f"Fetching events with auth_mode: {input.auth_mode} and filters.")
        
        # Determine the endpoint URL based on auth_mode
        if input.auth_mode == "me":
            url = "https://graph.microsoft.com/v1.0/me/events"
        elif input.auth_mode == "app":
            url = "https://graph.microsoft.com/v1.0/users/{user_id}/events"  # Replace `{user_id}` with the actual user ID for app authentication.
        else:
            raise ValueError("Invalid auth_mode. Supported values are 'app' and 'me'.")

        headers = {
            "Authorization": f"Bearer {input.access_token}",
            "Content-Type": "application/json",
        }

        # Construct query parameters for filtering
        params = {
            "$select": "id,subject,start,end,isOnlineMeeting,attendees,organizer,onlineMeeting",
            "$top": "50",
        }
        filter_clauses = []
        if input.subject_filter:
            filter_clauses.append(f"startswith(subject, '{input.subject_filter}')")
        if input.start_date:
            filter_clauses.append(f"start/dateTime ge '{input.start_date}'")
        if input.end_date:
            filter_clauses.append(f"end/dateTime le '{input.end_date}'")

        if filter_clauses:
            params["$filter"] = " and ".join(filter_clauses)

        logger.debug(f"Making GET request to URL: {url} with params: {params}")

        # Send the GET request
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            logger.info("Successfully fetched events.")
            return response.json()
        else:
            error_message = f"Error fetching events: {response.status_code} - {response.text}"
            logger.error(error_message)
            raise Exception(error_message)
    except Exception as e:
        logger.exception("An error occurred while fetching events.")
        raise e


from dotenv import load_dotenv

# Test Main Method
if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    # Replace with your actual access token
    access_token = os.getenv("ACCESS_TOKEN")
    
    # Calculate dates for the last week
    today = datetime.utcnow()
    one_week_ago = today - timedelta(days=7)
    start_date = one_week_ago.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
    end_date = today.replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + "Z"

    # Test input data
    input_data = FetchEventsInput(
        access_token=access_token,
        auth_mode="me",
        subject_filter="New Year Meeting 1",
        start_date="",
        end_date="",
    )
    
    try:
        logger.debug("Starting the event fetching process...")
        events = fetch_events(input_data)
        print("Fetched Events:\n")
        print(events)
    except Exception as e:
        logger.error(f"Error: {e}")