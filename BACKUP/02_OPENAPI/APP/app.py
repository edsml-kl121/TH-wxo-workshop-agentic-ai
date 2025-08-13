from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import base64
import json
import os
import re
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import gspread
from googleapiclient.discovery import build

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Gmail & Calendar API", version="1.0.0")

# Pydantic models for request bodies
class EmailRequest(BaseModel):
    to: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body content")
    cc: Optional[str] = Field(None, description="CC email addresses (comma-separated)")
    bcc: Optional[str] = Field(None, description="BCC email addresses (comma-separated)")

class CalendarEventRequest(BaseModel):
    title: str = Field(..., description="Event title")
    date: str = Field(..., description="Event date in YYYY-MM-DD format")
    time: str = Field(..., description="Event time (e.g., '18:00', '6pm', '6-8pm')")
    attendees: List[str] = Field(..., description="List of attendee email addresses")

class PlaceOrderRequest(BaseModel):
    product_name: str = Field(..., description="Product name")
    voucher_code: str = Field(..., description="Voucher Code")
    quantity: int = Field(..., description="Quantity ordered", gt=0)


# Character encoding helper functions
def decode_unicode_escapes(text):
    """Decode Unicode escape sequences in text only if they exist"""
    # Check if text contains Unicode escape sequences
    if '\\u' not in text and '\\n' not in text and '\\t' not in text:
        # No escape sequences found, return original text
        return text
    
    try:
        # Method 1: Use json.loads for proper Unicode handling
        import json
        json_string = f'"{text}"'
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError, ValueError):
        try:
            # Method 2: Use codecs.decode
            import codecs
            return codecs.decode(text, 'unicode_escape')
        except (UnicodeDecodeError, UnicodeEncodeError):
            # If all methods fail, return original text
            return text

def detect_and_convert_table(text):
    """Detect pipe-separated table data and convert to HTML table"""
    lines = text.split('\n')
    
    # Look for lines that contain multiple pipes (|) - likely table rows
    table_lines = []
    non_table_lines = []
    in_table = False
    
    for line in lines:
        stripped_line = line.strip()
        # Check if line looks like a table row (has multiple pipes)
        if stripped_line.count('|') >= 3:  # At least 3 pipes means likely table
            table_lines.append(stripped_line)
            in_table = True
        else:
            if in_table and table_lines:
                # Process the accumulated table
                html_table = convert_pipes_to_html_table(table_lines)
                non_table_lines.append(html_table)
                table_lines = []
                in_table = False
            non_table_lines.append(line)
    
    # Handle remaining table at end of text
    if table_lines:
        html_table = convert_pipes_to_html_table(table_lines)
        non_table_lines.append(html_table)
    
    return '\n'.join(non_table_lines)

def convert_pipes_to_html_table(table_lines):
    """Convert pipe-separated lines to HTML table"""
    if not table_lines:
        return ""
    
    html = '<table border="1" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; margin: 10px 0;">\n'
    
    for i, line in enumerate(table_lines):
        # Split by pipe and clean up
        cells = [cell.strip() for cell in line.split('|') if cell.strip()]
        
        if not cells:
            continue
            
        # First row is typically header
        tag = 'th' if i == 0 else 'td'
        style = 'style="padding: 8px; text-align: left; background-color: #f2f2f2; font-weight: bold;"' if i == 0 else 'style="padding: 8px; text-align: left;"'
        
        html += '  <tr>\n'
        for cell in cells:
            html += f'    <{tag} {style}>{cell}</{tag}>\n'
        html += '  </tr>\n'
    
    html += '</table>'
    return html

def should_send_as_html(text):
    """Determine if email should be sent as HTML based on content"""
    # Check for table-like content (multiple lines with pipes)
    lines = text.split('\n')
    table_line_count = sum(1 for line in lines if line.strip().count('|') >= 3)
    
    return table_line_count >= 2  # If 2+ lines look like table rows

# Gmail functionality
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailService:
    """Gmail service for sending emails with proper character encoding"""

    def __init__(self):
        self.service = None
        self._authenticate()

    def _authenticate(self):
        try:
            token_json = os.environ.get('GMAIL_TOKEN_JSON')
            if not token_json:
                raise ValueError("GMAIL_TOKEN_JSON environment variable not found")

            # Handle both JSON string and file path
            if token_json.startswith('{'):
                token_data = json.loads(token_json)
            else:
                with open(token_json, 'r') as f:
                    token_data = json.load(f)

            creds = Credentials.from_authorized_user_info(token_data, GMAIL_SCOPES)

            if creds.expired and creds.refresh_token:
                creds.refresh(Request())

            if not creds.valid:
                raise ValueError("Invalid Gmail credentials")

            self.service = build('gmail', 'v1', credentials=creds)
        except Exception as e:
            raise Exception(f"Gmail authentication failed: {e}")

    def send_email(self, to_email, subject, body, cc=None, bcc=None):
        try:
            if not self.service:
                raise Exception("Gmail service not initialized")

            # Decode Unicode escape sequences
            decoded_subject = decode_unicode_escapes(subject)
            decoded_body = decode_unicode_escapes(body)

            # Check if we should send as HTML
            if should_send_as_html(decoded_body):
                # Convert table content and send as HTML
                html_body = detect_and_convert_table(decoded_body)
                # Replace newlines with <br> for HTML
                html_body = html_body.replace('\n', '<br>\n')
                
                message = MIMEMultipart('alternative')
                message['to'] = to_email
                message['subject'] = decoded_subject
                
                if cc:
                    message['cc'] = cc
                if bcc:
                    message['bcc'] = bcc

                # Add plain text version
                text_part = MIMEText(decoded_body, 'plain', 'utf-8')
                message.attach(text_part)
                
                # Add HTML version
                html_part = MIMEText(html_body, 'html', 'utf-8')
                message.attach(html_part)
            else:
                # Send as plain text only but use MIMEMultipart for better encoding
                message = MIMEMultipart()
                message['to'] = to_email
                message['subject'] = decoded_subject
                
                if cc:
                    message['cc'] = cc
                if bcc:
                    message['bcc'] = bcc

                body_part = MIMEText(decoded_body, 'plain', 'utf-8')
                message.attach(body_part)

            # Encode message properly
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('ascii')
            
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            return {
                'success': True,
                'message_id': result['id'],
                'to': to_email,
                'subject': decoded_subject
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Calendar functionality
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']

def _convert_to_24hour(time_str):
    """Convert various time formats to 24-hour HH:MM format"""
    time_str = time_str.strip().lower()
    
    # Already in HH:MM format
    if re.match(r'^\d{1,2}:\d{2}$', time_str):
        parts = time_str.split(':')
        hour = int(parts[0])
        minute = int(parts[1])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"
    
    # Handle AM/PM format like "6pm", "6:30pm", "6 pm"
    am_pm_match = re.match(r'^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$', time_str)
    if am_pm_match:
        hour = int(am_pm_match.group(1))
        minute = int(am_pm_match.group(2)) if am_pm_match.group(2) else 0
        am_pm = am_pm_match.group(3)
        
        # Convert to 24-hour
        if am_pm == 'pm' and hour != 12:
            hour += 12
        elif am_pm == 'am' and hour == 12:
            hour = 0
        
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return f"{hour:02d}:{minute:02d}"
    
    # Handle just numbers like "6", "18"
    if re.match(r'^\d{1,2}$', time_str):
        hour = int(time_str)
        # Assume PM for single digit hours 1-11, 24-hour for 12-23
        if 1 <= hour <= 11:
            hour += 12  # Convert to PM
        elif hour == 12:
            hour = 12   # Keep as noon
        elif 0 <= hour <= 23:
            pass  # Already in 24-hour format
        else:
            return None
        
        return f"{hour:02d}:00"
    
    return None

def _parse_time_input(time_input):
    """Parse various time formats and return start_time and end_time in HH:MM format"""
    time_str = time_input.strip().lower()
    
    # Handle range formats like "6-8pm", "18:00-20:00", "6pm-8pm"
    if '-' in time_str:
        parts = time_str.split('-')
        if len(parts) == 2:
            start_part = parts[0].strip()
            end_part = parts[1].strip()
            
            # Convert to 24-hour format
            start_24 = _convert_to_24hour(start_part)
            end_24 = _convert_to_24hour(end_part)
            
            if start_24 and end_24:
                return start_24, end_24
    
    # Handle single time like "6pm", "18:00"
    start_24 = _convert_to_24hour(time_str)
    if start_24:
        # Default to 1-hour duration
        start_hour, start_min = map(int, start_24.split(':'))
        end_hour = start_hour + 1
        if end_hour >= 24:
            end_hour = 23
            end_min = 59
        else:
            end_min = start_min
        end_24 = f"{end_hour:02d}:{end_min:02d}"
        return start_24, end_24
    
    return None, None

def _create_calendar_event(title, date, time, attendees):
    """Create Google Calendar event with proper character encoding"""
    try:
        # Get token data from environment variable
        token_data = os.getenv("GOOGLE_CALENDAR_TOKEN_JSON")
        if not token_data:
            return {'success': False, 'error': 'GOOGLE_CALENDAR_TOKEN_JSON environment variable not found in .env file'}
        
        # Import Google libraries only when needed
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        
        # Check if token_data is a file path or JSON content
        if token_data.startswith('{'):
            # It's JSON content directly
            try:
                token_info = json.loads(token_data)
                creds = Credentials.from_authorized_user_info(token_info, CALENDAR_SCOPES)
            except json.JSONDecodeError as e:
                return {'success': False, 'error': f'Invalid JSON in GOOGLE_CALENDAR_TOKEN_JSON: {e}'}
        else:
            # It's a file path
            if not os.path.exists(token_data):
                return {'success': False, 'error': f'Token file not found at: {token_data}'}
            
            # Load credentials from file
            creds = Credentials.from_authorized_user_file(token_data, CALENDAR_SCOPES)
        
        # Refresh token if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # If it was from a file, save back to file
            if not token_data.startswith('{') and os.path.exists(token_data):
                with open(token_data, 'w') as token:
                    token.write(creds.to_json())
        
        # Build the Calendar API service
        service = build('calendar', 'v3', credentials=creds)
        
        # Parse time input to handle various formats
        start_time, end_time = _parse_time_input(time)
        if not start_time or not end_time:
            return {'success': False, 'error': f'Invalid time format: {time}. Use formats like "18:00", "6pm", "6-8pm", "18:00-20:00"'}
        
        # Decode Unicode escape sequences in title
        decoded_title = decode_unicode_escapes(title)
        
        # Create event object
        event = {
            'summary': decoded_title,
            'location': 'Conference Room A',
            'description': 'Meeting created via FastAPI',
            'start': {
                'dateTime': f'{date}T{start_time}:00+07:00',  # Bangkok timezone
                'timeZone': 'Asia/Bangkok',
            },
            'end': {
                'dateTime': f'{date}T{end_time}:00+07:00',  # Bangkok timezone
                'timeZone': 'Asia/Bangkok',
            },
            'attendees': [{'email': email} for email in attendees],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                    {'method': 'popup', 'minutes': 10},       # 10 minutes before
                ],
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': f'meet-{datetime.now().strftime("%Y%m%d%H%M%S")}',
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            }
        }
        
        # Create the event
        event_result = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()
        
        return {
            'success': True,
            'event_id': event_result['id'],
            'event_link': event_result['htmlLink'],
            'meet_link': event_result.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri', ''),
            'display_time': f'{start_time}-{end_time}'
        }
        
    except ImportError:
        return {'success': False, 'error': 'Google API libraries not available. Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_credentials():
    """
    Get OAuth2 credentials for Google Sheets
    Similar to Gmail authentication - supports both JSON string and file path
    """
    try:
        # Get token from environment variable (similar to Gmail pattern)
        token_json = os.environ.get('GGSHEETS_TOKEN_JSON')
        if not token_json:
            raise ValueError("GGSHEETS_TOKEN_JSON environment variable not found")

        # Handle both JSON string and file path
        if token_json.startswith('{'):
            # It's a JSON string directly
            token_data = json.loads(token_json)
            creds = Credentials.from_authorized_user_info(token_data, SHEETS_SCOPES)
        else:
            # It's a file path
            if not os.path.exists(token_json):
                raise FileNotFoundError(f"Token file not found at: {token_json}")
            
            with open(token_json, 'r') as f:
                token_data = json.load(f)
            creds = Credentials.from_authorized_user_info(token_data, SHEETS_SCOPES)
        
        # Check if credentials need refresh
        if creds.expired and creds.refresh_token:
            print("Refreshing expired Google Sheets token...")
            creds.refresh(Request())
            
            # If token was loaded from file, save the refreshed token back
            if not token_json.startswith('{') and os.path.exists(token_json):
                with open(token_json, 'w') as token:
                    token.write(creds.to_json())
                print("Refreshed token saved back to file.")
        
        if not creds.valid:
            raise ValueError("Invalid Google Sheets credentials")
        
        return creds
        
    except Exception as e:
        raise Exception(f"Google Sheets authentication failed: {e}")


# Google Sheets functionality
def append_to_sheets(data_rows):
    """
    Append data to Google Sheets using pre-generated token
    
    Args:
        data_rows (list): List of lists containing row data
    """
    try:
        creds = get_sheets_credentials()
        client = gspread.authorize(creds)
        
        # Use spreadsheet ID from environment variables
        sheet_id = os.getenv("GGSHEETS_ID")
        if not sheet_id:
            raise ValueError("GGSHEETS_ID environment variable not found")
        
        sheet = client.open_by_key(sheet_id).sheet1
        sheet.append_rows(data_rows)
        return True
    except Exception as e:
        raise Exception(f"Failed to append to Google Sheets: {str(e)}")
    

# API Routes
@app.post("/send_gmail")
async def send_gmail(email_request: EmailRequest):
    """
    Send email via Gmail with proper character encoding support
    """
    try:
        gmail_service = GmailService()
        result = gmail_service.send_email(
            to_email=email_request.to,
            subject=email_request.subject,
            body=email_request.body,
            cc=email_request.cc,
            bcc=email_request.bcc
        )

        if result['success']:
            return {
                "status": "success",
                "message": "Email sent successfully",
                "data": {
                    "message_id": result['message_id'],
                    "to": email_request.to,
                    "subject": result['subject'],  # Use decoded subject
                    "cc": email_request.cc or "-",
                    "bcc": email_request.bcc or "-"
                }
            }
        else:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {result['error']}")

    except Exception as e:
        # Fallback to simulation mode with decoded content
        decoded_subject = decode_unicode_escapes(email_request.subject)
        decoded_body = decode_unicode_escapes(email_request.body)
        
        return {
            "status": "simulation",
            "message": "Email simulation mode (due to authentication error)",
            "data": {
                "to": email_request.to,
                "subject": decoded_subject,
                "body": decoded_body,
                "cc": email_request.cc or "-",
                "bcc": email_request.bcc or "-",
                "error": str(e)
            }
        }

@app.post("/create_calendar_event")
async def create_calendar_event(event_request: CalendarEventRequest):
    """
    Create Google Calendar event with Google Meet and proper character encoding
    """
    try:
        result = _create_calendar_event(
            title=event_request.title,
            date=event_request.date,
            time=event_request.time,
            attendees=event_request.attendees
        )

        if result and result.get('success'):
            return {
                "status": "success",
                "message": "Calendar event created successfully",
                "data": {
                    "title": decode_unicode_escapes(event_request.title),
                    "date": event_request.date,
                    "time": result.get('display_time', event_request.time),
                    "attendees": event_request.attendees,
                    "event_id": result.get('event_id', ''),
                    "event_link": result.get('event_link', ''),
                    "meet_link": result.get('meet_link', ''),
                    "timezone": "Asia/Bangkok"
                }
            }
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
            return {
                "status": "error",
                "message": "Failed to create calendar event",
                "data": {
                    "title": decode_unicode_escapes(event_request.title),
                    "date": event_request.date,
                    "time": event_request.time,
                    "attendees": event_request.attendees,
                    "error": error_msg,
                    "simulation_link": "https://meet.google.com/mock-link-1234"
                }
            }

    except Exception as e:
        return {
            "status": "error",
            "message": "Exception occurred while creating calendar event",
            "data": {
                "title": decode_unicode_escapes(event_request.title),
                "date": event_request.date,
                "time": event_request.time,
                "attendees": event_request.attendees,
                "error": str(e),
                "simulation_link": "https://meet.google.com/mock-link-1234"
            }
        }

@app.post("/place_order")
async def place_order(order_request: PlaceOrderRequest):
    """
    Place an order and save it to Google Sheets
    """
    try:
        # Mock customer data only
        mock_customers = [
            {"name": "John Doe", "email": "john.doe@email.com"},
            # {"name": "Jane Smith", "email": "jane.smith@email.com"},
            # {"name": "Mike Johnson", "email": "mike.johnson@email.com"},
            # {"name": "Sarah Wilson", "email": "sarah.wilson@email.com"},
            # {"name": "David Brown", "email": "david.brown@email.com"}
        ]
        
        # Generate random mock data
        import random
        selected_customer = random.choice(mock_customers)
        
        # Generate order ID
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Prepare data for Google Sheets
        # Only include: Order ID, Date, Product, Quantity
        order_data = [
            [
                order_id,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                decode_unicode_escapes(order_request.product_name),
                decode_unicode_escapes(order_request.voucher_code),
                order_request.quantity
            ]
        ]
        
        # Append to Google Sheets
        try:
            append_to_sheets(order_data)
            sheets_status = "success"
            sheets_error = None
        except Exception as sheets_error:
            sheets_status = "error"
            sheets_error = str(sheets_error)
        
        return {
            "status": "success" if sheets_status == "success" else "partial_success",
            "message": "Order placed successfully" if sheets_status == "success" else "Order processed but failed to save to sheets",
            "data": {
                "order_id": order_id,
                # "customer_name": selected_customer["name"],
                "product_name": decode_unicode_escapes(order_request.product_name),
                "quantity": order_request.quantity,
                # "customer_email": selected_customer["email"],
                "order_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "sheets_status": sheets_status,
                "sheets_error": sheets_error
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to place order",
            "data": {
                "product_name": decode_unicode_escapes(order_request.product_name),
                "quantity": order_request.quantity,
                "error": str(e)
            }
        }

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Gmail & Calendar FastAPI Service",
        "version": "1.0.0",
        "endpoints": {
            "send_gmail": "POST /send_gmail",
            "create_calendar_event": "POST /create_calendar_event"
        },
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)