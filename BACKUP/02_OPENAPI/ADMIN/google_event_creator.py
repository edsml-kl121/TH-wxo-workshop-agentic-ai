# Google Calendar API - Create Event (Python)
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# File paths
TOKEN_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def load_credentials():
    """Load and return valid credentials"""
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(f"Token file {TOKEN_FILE} not found. Run token generation first.")
    
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Refresh token if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def create_calendar_event(event_details):
    """Create a calendar event"""
    try:
        # Load credentials
        creds = load_credentials()
        
        # Build the Calendar API service
        service = build('calendar', 'v3', credentials=creds)
        
        # Create event object
        event = {
            'summary': event_details.get('title', 'New Event'),
            'location': event_details.get('location', ''),
            'description': event_details.get('description', ''),
            'start': {
                'dateTime': event_details['start_datetime'],
                'timeZone': event_details.get('timezone', 'America/Los_Angeles'),
            },
            'end': {
                'dateTime': event_details['end_datetime'],
                'timeZone': event_details.get('timezone', 'America/Los_Angeles'),
            },
            'attendees': event_details.get('attendees', []),
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                    {'method': 'popup', 'minutes': 10},       # 10 minutes before
                ],
            },
        }
        
        # Add recurrence if specified
        if 'recurrence' in event_details:
            event['recurrence'] = event_details['recurrence']
        
        # Create the event
        event_result = service.events().insert(
            calendarId='primary',  # Use 'primary' for main calendar
            body=event
        ).execute()
        
        print("Event created successfully!")
        print(f"Event ID: {event_result['id']}")
        print(f"Event Link: {event_result['htmlLink']}")
        
        return event_result
        
    except Exception as e:
        print(f"Error creating event: {e}")
        raise

def format_datetime(year, month, day, hour, minute, timezone='America/Los_Angeles'):
    """Helper function to format datetime for Google Calendar"""
    dt = datetime(year, month, day, hour, minute)
    # Format as ISO string with timezone
    if timezone == 'UTC':
        return dt.isoformat() + 'Z'
    else:
        # For non-UTC timezones, use the format without Z
        return dt.isoformat()

def create_recurring_event(event_details, recurrence_rule):
    """Create a recurring event"""
    event_details['recurrence'] = [recurrence_rule]
    return create_calendar_event(event_details)

# Example usage
def main():
    # Example 1: Simple event
    event_details = {
        'title': 'watsonx Orchestrate Team Meeting',
        'location': 'Conference Room A',
        'description': 'Weekly team sync meeting',
        'start_datetime': '2025-06-25T10:00:00+07:00',  # Bangkok is UTC+7
        'end_datetime': '2025-06-25T11:00:00+07:00',    # Bangkok is UTC+7
        'timezone': 'Asia/Bangkok',
        'attendees': [
            {'email': 'mew.chayutaphong@gmail.com'},
            {'email': 'Kandanai.Leenutaphong@ibm.com'}
        ]
    }
    
    try:
        event = create_calendar_event(event_details)
        print(f"Created event: {event['summary']}")
    except Exception as e:
        print(f"Failed to create event: {e}")
    
    # # Example 2: Recurring event (every week for 4 weeks)
    # recurring_event_details = {
    #     'title': 'Weekly Standup',
    #     'location': 'Zoom Meeting',
    #     'description': 'Daily standup meeting',
    #     'start_datetime': '2024-12-26T09:00:00-08:00',
    #     'end_datetime': '2024-12-26T09:30:00-08:00',
    #     'timezone': 'America/Los_Angeles'
    # }
    
    # try:
    #     recurring_event = create_recurring_event(
    #         recurring_event_details, 
    #         'RRULE:FREQ=WEEKLY;COUNT=4'  # Every week for 4 weeks
    #     )
    #     print(f"Created recurring event: {recurring_event['summary']}")
    # except Exception as e:
    #     print(f"Failed to create recurring event: {e}")

# Additional utility functions
def list_upcoming_events(max_results=10):
    """List upcoming events"""
    try:
        creds = load_credentials()
        service = build('calendar', 'v3', credentials=creds)
        
        # Get current time
        now = datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
            return []
        
        print(f'Upcoming {len(events)} events:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"- {event['summary']} ({start})")
        
        return events
        
    except Exception as e:
        print(f"Error listing events: {e}")
        return []

if __name__ == "__main__":
    main()