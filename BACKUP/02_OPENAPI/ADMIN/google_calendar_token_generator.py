# Google Calendar API - Token Generation (Python)
# First, install required packages: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# OAuth2 credentials (get these from Google Cloud Console)
# Create a credentials.json file with your OAuth2 client configuration
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# Scopes for calendar access
SCOPES = ['https://www.googleapis.com/auth/calendar']

def generate_token():
    """Generate and save OAuth2 token for Google Calendar API"""
    creds = None
    
    # Check if token file already exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired token
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            # Generate new token
            print("Generating new token...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        print(f"Token saved to {TOKEN_FILE}")
    
    return creds

def load_token():
    """Load existing token from file"""
    try:
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            if creds.valid:
                return creds
            elif creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Save refreshed token
                with open(TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
                return creds
        return None
    except Exception as e:
        print(f"Error loading token: {e}")
        return None

def create_credentials_file():
    """Helper function to create credentials.json template"""
    credentials_template = {
        "installed": {
            "client_id": "your-client-id.googleusercontent.com",
            "project_id": "your-project-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "your-client-secret",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    with open('credentials_template.json', 'w') as f:
        json.dump(credentials_template, f, indent=2)
    
    print("Created credentials_template.json")
    print("Replace the placeholder values with your actual OAuth2 credentials")
    print("Then rename it to credentials.json")

if __name__ == "__main__":
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Credentials file {CREDENTIALS_FILE} not found!")
        create_credentials_file()
        print("Please set up your credentials.json file first.")
    else:
        try:
            creds = generate_token()
            if creds:
                print("Token generated successfully!")
            else:
                print("Failed to generate token")
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure your credentials.json file is properly configured")