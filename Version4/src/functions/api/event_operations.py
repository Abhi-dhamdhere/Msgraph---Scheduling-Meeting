from functions.api.api_utility import make_request
from typing import Dict, Any

def get_calendar_events(access_token: str) -> dict:
    """
    Retrieves a user's calendar events.
    :param access_token: OAuth token for authenticating with the Microsoft Graph API.
    :return: JSON response containing calendar events.
    """
    url = "https://graph.microsoft.com/v1.0/me/events"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    return make_request(url, "GET", headers)


def create_event(access_token: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a calendar event with priority, location, and online meeting options.
    """
    url = "https://graph.microsoft.com/v1.0/me/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    return make_request(url, "POST", headers, event_data)


def update_event(access_token: str, event_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates a calendar event, supporting partial updates.
    """
    url = f"https://graph.microsoft.com/v1.0/me/events/{event_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    return make_request(url, "PATCH", headers, event_data)


def find_meeting_times(
    access_token: str,
    attendees: list,
    meeting_duration: str,
    max_candidates: int = 5,
    is_online_meeting: bool = True,
    online_meeting_provider: str = "Teams"
) -> Dict[str, Any]:
    """
    Finds optimal meeting times with online meeting options.
    """
    url = "https://graph.microsoft.com/v1.0/me/findMeetingTimes"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "attendees": attendees,
        "meetingDuration": meeting_duration,
        "maxCandidates": max_candidates,
        "isOrganizerOptional": False,
        "returnSuggestionReasons": True,
        "isOnlineMeeting": is_online_meeting,
        "onlineMeetingProvider": online_meeting_provider
    }
    return make_request(url, "POST", headers, payload)
