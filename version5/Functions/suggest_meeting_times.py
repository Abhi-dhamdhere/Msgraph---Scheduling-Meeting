# Author: Abhishek Ravindra Dhamdhere
# Email: dhamdhereabhishek16@gmail.com
# Phone: 9594709185
# Organization: DisruptiveNext
# Supervisor: Mr. Prashant Mane

# Description: 
# This script is part of an internship task aimed at simplifying meeting scheduling 
# across different time zones. It integrates with the Microsoft Graph API to interact with the user's calendar 
# and fetch, modify, or schedule events. Authentication is handled using MSAL (Microsoft Authentication Library) 
# through the device code flow to obtain an access token. 

# The script allows for:
# - Fetching existing calendar events filtered by subject, start date, and end date.
# - Checking for event overlap before scheduling a new meeting.
# - Suggesting available meeting times based on attendee availability.
# - Scheduling a meeting with selected times and attendees.

# For each scheduled meeting, the script can also provide options to modify, delete, or cancel events 
# after the meeting is created.

# This app ensures efficient handling of time zone differences and prevents scheduling conflicts, 
# making it easier to organize meetings across multiple time zones.

# Trello Card Link: https://trello.com/c/q26wAMWs

import os
import json
import requests
import sys
from dotenv import load_dotenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from logger_utility import setup_logger



# Load environment variables
load_dotenv()

# Initialize environment variables
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Ensure ACCESS_TOKEN is available
if not ACCESS_TOKEN:
    print("Access token is missing in .env file.")
    sys.exit(1)

# Initialize Logger
logger = setup_logger()

# Function to load meeting data from a JSON file
def load_meeting_data(file_path="meeting_data.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error reading JSON file: {e}")
        return None

# Function to suggest meeting times
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
            print("Suggested meeting times:", response.json())
        else:
            logger.error(f"Error suggesting meeting times: {response.status_code} - {response.text}")
            print(f"Error suggesting meeting times: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"Error suggesting meeting times: {e}")
        print(f"Error suggesting meeting times: {e}")

# Load meeting data from JSON file
meeting_data = load_meeting_data()

if meeting_data:
    # Call the function to suggest meeting times
    suggest_meeting_times(meeting_data)
else:
    print("Failed to load meeting data.")
