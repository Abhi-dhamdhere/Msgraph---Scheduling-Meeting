import unittest
from unittest.mock import patch
from scheduling_meeting import create_event, update_event, find_meeting_times, APIError


class TestAPICalls(unittest.TestCase):
    @patch("scheduling_meeting.make_request")
    def test_create_event_success(self, mock_make_request):
        # Mock the API response
        mock_make_request.return_value = {"id": "event123", "subject": "Test Event"}

        # Call the function
        access_token = "mock_access_token"
        event_data = {"subject": "Test Event", "start": {}, "end": {}}
        response = create_event(access_token, event_data)

        # Assertions
        self.assertEqual(response["id"], "event123")
        self.assertEqual(response["subject"], "Test Event")
        mock_make_request.assert_called_once()

    @patch("scheduling_meeting.make_request")
    def test_update_event_success(self, mock_make_request):
        # Mock the API response
        mock_make_request.return_value = {"id": "event123", "subject": "Updated Event"}

        # Call the function
        access_token = "mock_access_token"
        event_id = "event123"
        event_data = {"subject": "Updated Event"}
        response = update_event(access_token, event_id, event_data)

        # Assertions
        self.assertEqual(response["id"], "event123")
        self.assertEqual(response["subject"], "Updated Event")
        mock_make_request.assert_called_once()

    @patch("scheduling_meeting.make_request")
    def test_find_meeting_times_success(self, mock_make_request):
        # Mock the API response
        mock_make_request.return_value = {"meetingTimeSuggestions": []}

        # Call the function
        access_token = "mock_access_token"
        attendees = [{"emailAddress": {"address": "test@example.com"}, "type": "required"}]
        meeting_duration = "PT1H"
        response = find_meeting_times(access_token, attendees, meeting_duration)

        # Assertions
        self.assertIn("meetingTimeSuggestions", response)
        mock_make_request.assert_called_once()

    @patch("scheduling_meeting.make_request")
    def test_api_call_failure(self, mock_make_request):
        # Simulate an API error
        mock_make_request.side_effect = APIError("API request failed", status_code=400)

        access_token = "mock_access_token"
        event_data = {"subject": "Test Event"}

        with self.assertRaises(APIError):
            create_event(access_token, event_data)


if __name__ == "__main__":
    unittest.main()
