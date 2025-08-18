"""
Gmail Tool for watsonx orchestrate
No Google Workspace required - works with any Gmail account
"""

import base64
import json
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
# Set the token as environment variable (copy from your output above)
# Set environment variable
# os.environ['GMAIL_TOKEN_JSON'] = os.getenv("GMAIL_TOKEN_JSON")

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class WatsonxGmailTool:
    """Gmail tool for watsonx orchestrate"""
    
    def __init__(self):
        """Initialize with environment token"""
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate using environment token"""
        try:
            # Get token from environment variable
            token_json = os.environ.get('GMAIL_TOKEN_JSON')
            
            if not token_json:
                raise ValueError("GMAIL_TOKEN_JSON environment variable not found")
            
            # Parse token
            token_data = json.loads(token_json)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            
            # Refresh if expired (works without browser)
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            if not creds.valid:
                raise ValueError("Invalid credentials")
            
            # Build Gmail service
            self.service = build('gmail', 'v1', credentials=creds)
            
        except Exception as e:
            raise Exception(f"Gmail authentication failed: {e}")
    
    def send_email(self, to_email, subject, body, is_html=False, from_name=None):
        """
        Send email via Gmail
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Email content
            is_html (bool): Whether body is HTML
            from_name (str): Optional sender name
        
        Returns:
            dict: Result with success status
        """
        try:
            if not self.service:
                raise Exception("Gmail service not initialized")
            
            # Create message
            if is_html:
                message = MIMEText(body, 'html')
            else:
                message = MIMEText(body, 'plain')
            
            message['to'] = to_email
            message['subject'] = subject
            
            if from_name:
                message['from'] = from_name
            
            # Encode and send
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return {
                'success': True,
                'message_id': result['id'],
                'to': to_email,
                'subject': subject
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Main functions for watsonx orchestrate
def send_gmail(recipient, subject, message, html=False):
    """
    Send Gmail - Main function for watsonx orchestrate
    
    Args:
        recipient (str): Email recipient
        subject (str): Email subject
        message (str): Email body
        html (bool): Send as HTML email
    
    Returns:
        str: Success or error message
    """
    try:
        gmail_tool = WatsonxGmailTool()
        result = gmail_tool.send_email(recipient, subject, message, html)
        
        if result['success']:
            return f"✅ Email sent successfully to {recipient}"
        else:
            return f"❌ Failed to send email: {result['error']}"
            
    except Exception as e:
        return f"❌ Gmail tool error: {str(e)}"

# def send_notification_email(recipient, title, notification_message):
#     """
#     Send formatted notification email
    
#     Args:
#         recipient (str): Email recipient
#         title (str): Notification title
#         notification_message (str): Notification content
    
#     Returns:
#         str: Success or error message
#     """
#     html_template = f"""
#     <html>
#         <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
#             <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0;">
#                 <h2 style="margin: 0; font-size: 24px;">🔔 {title}</h2>
#             </div>
#             <div style="background-color: #f8f9fa; padding: 20px; border-radius: 0 0 8px 8px;">
#                 <div style="background-color: white; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
#                     <p style="color: #333; line-height: 1.6; margin: 0; font-size: 16px;">{notification_message}</p>
#                 </div>
#                 <p style="color: #888; font-size: 12px; margin-top: 15px; text-align: center;">
#                     📧 This notification was sent via watsonx orchestrate
#                 </p>
#             </div>
#         </body>
#     </html>
#     """
    
#     return send_gmail(recipient, title, html_template, html=True)

# def send_report_email(recipient, report_title, report_data):
#     """
#     Send formatted report email
    
#     Args:
#         recipient (str): Email recipient
#         report_title (str): Report title
#         report_data (str): Report content/data
    
#     Returns:
#         str: Success or error message
#     """
#     html_report = f"""
#     <html>
#         <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
#             <div style="background-color: #2c3e50; color: white; padding: 25px; border-radius: 8px 8px 0 0;">
#                 <h1 style="margin: 0; font-size: 28px;">📊 {report_title}</h1>
#                 <p style="margin: 10px 0 0 0; opacity: 0.9;">Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
#             </div>
#             <div style="background-color: #ecf0f1; padding: 30px; border-radius: 0 0 8px 8px;">
#                 <div style="background-color: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
#                     <pre style="white-space: pre-wrap; font-family: 'Courier New', monospace; background-color: #f8f9fa; padding: 20px; border-radius: 4px; border-left: 4px solid #3498db; line-height: 1.4;">{report_data}</pre>
#                 </div>
#                 <p style="color: #7f8c8d; font-size: 12px; margin-top: 20px; text-align: center;">
#                     🤖 Report generated and sent via watsonx orchestrate
#                 </p>
#             </div>
#         </body>
#     </html>
#     """
    
#     return send_gmail(recipient, f"📊 {report_title}", html_report, html=True)

def check_gmail_status():
    """
    Check if Gmail tool is properly configured
    
    Returns:
        str: Status message
    """
    try:
        gmail_tool = WatsonxGmailTool()
        return "✅ Gmail tool is properly configured and ready to use"
    except Exception as e:
        return f"❌ Gmail tool configuration error: {str(e)}"

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing watsonx Gmail Tool...")
    
    # Check status
    status = check_gmail_status()
    print(f"Status: {status}")
    
    if "✅" in status:
        # Test basic email
        test_result = send_gmail(
            recipient="mew.chayutaphong@gmail.com",
            subject="Test from watsonx",
            message="Hello! This is a test email from watsonx orchestrate Gmail tool."
        )
        print(f"Test result: {test_result}")
        
        # Test notification
        # notification_result = send_notification_email(
        #     recipient="mew.chayutaphong@gmail.com",
        #     title="System Alert",
        #     notification_message="Your automated process completed successfully at 14:30."
        # )
        # print(f"Notification result: {notification_result}")
        # report_result = send_report_email(
        #     recipient="mew.chayutaphong@gmail.com",
        #     report_title="System Alert",
        #     report_data="Your automated process completed successfully at 14:30."
        # )
        # print(f"send_report_email result: {report_result}")
    else:
        print("❌ Gmail tool not configured properly")
        print("💡 Make sure GMAIL_TOKEN_JSON environment variable is set")