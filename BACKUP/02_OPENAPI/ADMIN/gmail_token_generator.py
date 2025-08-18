"""
Gmail Token Generator
Run this script ONCE on your local machine to generate authentication token
Then use the token in your watsonx orchestrate environment
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def generate_gmail_token():
    """Generate Gmail authentication token for server use"""
    
    print("🔑 Gmail Token Generator")
    print("=" * 40)
    
    # Check for credentials file
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("\n📥 Please download OAuth credentials from Google Cloud Console:")
        print("   1. Go to console.cloud.google.com")
        print("   2. APIs & Services → Credentials")
        print("   3. Create OAuth 2.0 Client ID")
        print("   4. Select 'Desktop application'")
        print("   5. Download as 'credentials.json'")
        return False
    
    try:
        print("🌐 Starting OAuth flow...")
        print("📖 A browser window will open for authentication")
        
        # Create OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        
        # Run OAuth flow (opens browser)
        creds = flow.run_local_server(
            port=0,
            prompt='select_account',
            access_type='offline'
        )
        
        # Save token to file
        token_data = creds.to_json()
        with open('token.json', 'w') as token_file:
            token_file.write(token_data)
        
        print("\n✅ Authentication successful!")
        print("💾 Token saved to token.json")
        
        # Display token for environment variable
        print("\n" + "=" * 60)
        print("🔧 FOR WATSONX ORCHESTRATE:")
        print("Copy this token and set as environment variable")
        print("=" * 60)
        print("Environment Variable Name: GMAIL_TOKEN_JSON")
        print("Environment Variable Value:")
        print(token_data)
        print("=" * 60)
        
        # Test the token
        print("\n🧪 Testing token...")
        test_email = input("📧 Enter test email address (or press Enter to skip): ").strip()
        
        if test_email:
            success = test_gmail_sending(token_data, test_email)
            if success:
                print("🎉 Test email sent successfully!")
                print("✅ Your setup is ready for watsonx orchestrate!")
            else:
                print("❌ Test email failed. Check your setup.")
        
        return True
        
    except FileNotFoundError:
        print("❌ credentials.json file not found in current directory")
        return False
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        return False

def test_gmail_sending(token_data, test_email):
    """Test email sending with generated token"""
    try:
        import base64
        from email.mime.text import MIMEText
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        # Create credentials from token
        token_dict = json.loads(token_data)
        creds = Credentials.from_authorized_user_info(token_dict, SCOPES)
        
        # Build Gmail service
        service = build('gmail', 'v1', credentials=creds)
        
        # Create test message
        message = MIMEText("🎉 Congratulations! Your Gmail API integration is working perfectly. This test email was sent using your generated token.")
        message['to'] = test_email
        message['subject'] = "✅ Gmail API Test - Success!"
        
        # Send email
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        return True
        
    except Exception as e:
        print(f"Test email error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Gmail token generation...")
    
    # Install required packages reminder
    print("\n📦 Make sure you have installed required packages:")
    print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    
    input("\n👆 Press Enter when packages are installed...")
    
    # Generate token
    success = generate_gmail_token()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. ✅ Token generated successfully")
        print("2. 📋 Copy the GMAIL_TOKEN_JSON value above")
        print("3. 🔧 Set it as environment variable in watsonx orchestrate")
        print("4. 🚀 Use the watsonx Gmail tool!")
    else:
        print("\n💥 Setup failed. Please check the steps above.")
    
    input("\nPress Enter to exit...")