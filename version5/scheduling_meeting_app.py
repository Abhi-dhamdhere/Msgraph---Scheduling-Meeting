import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import requests
from pytz import timezone, UTC
from Functions.fetch_events import fetch_events, FetchEventsInput
from Functions.modify_event import modify_event  # Import modify_event function
from Functions.delete_event import delete_event  # Import delete_event function
from Functions.cancel_event import cancel_event  # Import cancel_event function
from logger_utility import setup_logger

# Load environment variables
load_dotenv()

# Initialize environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Initialize Logger
logger = setup_logger()

# Function to read the meeting details from the JSON file
def load_meeting_data(file_path="schedule_meeting.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error reading JSON file: {e}")
        return None

# Convert local time to UTC
def convert_to_utc(local_time_str, time_zone_str):
    try:
        local_time = datetime.fromisoformat(local_time_str)
        local_tz = timezone(time_zone_str)
        local_time = local_tz.localize(local_time)
        utc_time = local_time.astimezone(UTC)
        return utc_time.isoformat()
    except Exception as e:
        logger.error(f"Error converting to UTC: {e}")
        return None

# Function to check for overlapping events
def check_event_overlap(start_time, end_time):
    try:
        # Prepare input data for fetch_events
        input_data = FetchEventsInput(
            access_token=ACCESS_TOKEN,
            auth_mode="me",  # Assuming we're scheduling for the authenticated user
            start_date=start_time.isoformat() + "Z",
            end_date=end_time.isoformat() + "Z"
        )

        # Fetch existing events
        events = fetch_events(input_data)

        if events:
            logger.info(f"Found {len(events)} events during the proposed time frame.")
            return True  # Events overlap
        else:
            logger.info("No overlapping events found.")
            return False  # No overlap
    except Exception as e:
        logger.error(f"Error checking for event overlap: {e}")
        return False

# Function to schedule the meeting using Microsoft Graph API
def schedule_meeting(meeting_data):
    try:
        url = "https://graph.microsoft.com/v1.0/me/events"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        # Send POST request to create a new event
        response = requests.post(url, headers=headers, json=meeting_data)

        if response.status_code == 201:
            logger.info("Meeting successfully scheduled!")
            print("Meeting successfully scheduled!")
            return response.json()  # Return the event details including event ID
        else:
            logger.error(f"Error scheduling meeting: {response.status_code} - {response.text}")
            print(f"Error scheduling meeting: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error scheduling meeting: {e}")
        print(f"Error scheduling meeting: {e}")
        return None

# Function to load meeting data from a JSON file (suggested meeting times data)
def load_suggested_meeting_data(file_path="meeting_time_data.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error reading meeting time JSON file: {e}")
        return None

# Function to suggest meeting times using Microsoft Graph API
def suggest_meeting_times(meeting_data):
    url = "https://graph.microsoft.com/v1.0/me/findMeetingTimes"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # Send POST request to find meeting times
        response = requests.post(url, headers=headers, json=meeting_data)

        if response.status_code == 200:
            logger.info("Successfully retrieved meeting times.")
            suggested_times = response.json()
            print("Suggested meeting times:", suggested_times)
            return suggested_times
        else:
            logger.error(f"Error suggesting meeting times: {response.status_code} - {response.text}")
            print(f"Error suggesting meeting times: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error suggesting meeting times: {e}")
        print(f"Error suggesting meeting times: {e}")
        return None

def main():
    meeting_data = load_meeting_data()

    if not meeting_data:
        logger.error("No meeting data found to schedule.")
        return

    # Extract meeting details from JSON data
    subject = meeting_data.get("subject")
    start_time = datetime.fromisoformat(meeting_data["start"]["dateTime"])
    end_time = datetime.fromisoformat(meeting_data["end"]["dateTime"])
    attendees = [attendee["emailAddress"]["address"] for attendee in meeting_data["attendees"]]
    description = meeting_data["body"]["content"]

    # Check for overlapping events
    if check_event_overlap(start_time, end_time):
        logger.error("Unable to schedule meeting due to overlap with existing events.")
        print("Unable to schedule meeting due to overlap with existing events.")
        return

    # If no overlap, proceed to suggest meeting times
    suggested_times_data = load_suggested_meeting_data()

    if not suggested_times_data:
        logger.error("No suggested meeting data found.")
        return

    suggested_times = suggest_meeting_times(suggested_times_data)

    if not suggested_times:
        return

    # Assuming you select the first available suggested time
    selected_time = suggested_times.get("meetingTimeSlots", [])[0] if "meetingTimeSlots" in suggested_times else None

    if not selected_time:
        logger.error("No valid suggested times found.")
        return

    # Convert the selected time to UTC
    selected_start_time = convert_to_utc(selected_time["start"]["dateTime"], meeting_data["start"]["timeZone"])
    selected_end_time = convert_to_utc(selected_time["end"]["dateTime"], meeting_data["end"]["timeZone"])

    if not selected_start_time or not selected_end_time:
        logger.error("Error converting selected times to UTC.")
        return

    # Add the selected time to the meeting data
    meeting_data["start"]["dateTime"] = selected_start_time
    meeting_data["end"]["dateTime"] = selected_end_time

    # Proceed to schedule the meeting
    event_data = schedule_meeting(meeting_data)

    if not event_data:
        return

    event_id = event_data.get("id")

    # Example operations: modify, delete, or cancel the event after scheduling
    # Example of modifying an event
    new_meeting_data = load_meeting_data("modify_existing_event.json")  # Modify data can come from a different JSON file
    if new_meeting_data:
        modify_event(event_id, new_meeting_data)

    # Example of deleting the event
    # delete_event(event_id)

    # Example of cancelling the event
    # cancel_event(event_id)

if __name__ == "__main__":
    main()
