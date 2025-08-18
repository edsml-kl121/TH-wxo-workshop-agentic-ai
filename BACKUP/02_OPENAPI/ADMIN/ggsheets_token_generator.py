"""
Google Sheets Token Generator
Run this script once to generate the token.json file for Google Sheets API access.
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Google Sheets functionality
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

CREDENTIALS_FILE = 'credentials_26.json'
TOKEN_FILE = 'ggsheet_token.json'

def generate_token():
    """Generate OAuth2 token for Google Sheets"""
    print("=== Google Sheets Token Generator ===")
    
    # Check if credentials.json exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Error: {CREDENTIALS_FILE} not found!")
        print("Please download your OAuth2 credentials from Google Cloud Console")
        print("and save it as 'credentials.json' in the same directory.")
        return False
    
    # Check if token already exists
    if os.path.exists(TOKEN_FILE):
        print(f"Token file {TOKEN_FILE} already exists.")
        response = input("Do you want to regenerate it? (y/n): ").lower().strip()
        if response != 'y':
            print("Token generation cancelled.")
            return False
    
    try:
        print(f"Reading credentials from {CREDENTIALS_FILE}...")
        
        # Create OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE, SHEETS_SCOPES)
        
        print("Starting OAuth flow...")
        print("Your browser will open for authentication.")
        print("Please authorize the application to access your Google Sheets.")
        
        # Run OAuth flow
        creds = flow.run_local_server(port=0)
        
        # Save credentials to token file
        print(f"Saving token to {TOKEN_FILE}...")
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        print("✅ Token generated successfully!")
        print(f"Token saved to: {TOKEN_FILE}")
        print("You can now use this token in your FastAPI application.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating token: {e}")
        return False

def verify_token():
    """Verify that the token is valid"""
    if not os.path.exists(TOKEN_FILE):
        print(f"❌ Token file {TOKEN_FILE} not found!")
        return False
    
    try:
        print("Verifying token...")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SHEETS_SCOPES)
        
        if creds and creds.valid:
            print("✅ Token is valid!")
            return True
        elif creds and creds.expired and creds.refresh_token:
            print("Token expired, attempting to refresh...")
            creds.refresh(Request())
            
            # Save refreshed token
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            
            print("✅ Token refreshed successfully!")
            return True
        else:
            print("❌ Token is invalid!")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying token: {e}")
        return False

def main():
    """Main function"""
    print("Choose an option:")
    print("1. Generate new token")
    print("2. Verify existing token")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1':
        success = generate_token()
        if success:
            verify_token()
    elif choice == '2':
        verify_token()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()