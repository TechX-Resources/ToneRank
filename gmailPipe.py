# Data utility class for storing emails
# @author Rylan Ahmadi (Ry305)
# Last updated 06/12/2025

from googleapiclient.discovery import build
import base64
from myEmail import Email
from datetime import datetime, timedelta
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GmailPipe: 

    @staticmethod
    def get_gmail_service():
        """ Creates and returns a service for the gmail API. If necessary, refreshes credentials. """
        try:
            # Load credentials
            from google.oauth2.credentials import Credentials
            creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.readonly'])
            # Check if credentials have expired and refresh if needed
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Save the refreshed credentials
                GmailPipe._save_credentials(creds)
            elif creds.expired and not creds.refresh_token:
                raise Exception("Token expired and no refresh token is available")
            service = build('gmail', 'v1', credentials=creds)
            return service
        except Exception as e:
            GmailPipe.reauthorize_gmail()
            service = build('gmail', 'v1', credentials=creds)
            return service
    
    def reauthorize_gmail():
        """ Re-authorize the Gmail API to get fresh credentials with refresh token.
        Make sure you have credentials.json (OAuth client credentials) in the same directory. """
        
        # Define the scopes you need
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        
        try:
            # Create the flow using the client secrets file
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',  # Make sure this file exists
                SCOPES
            )
            
            # Run the OAuth flow to get credentials
            # access_type='offline' ensures we get a refresh token
            # prompt='consent' forces the consent screen to appear
            creds = flow.run_local_server(
                port=0,
                access_type='offline',
                prompt='consent'
            )
            
            # Save the credentials to token.json
            creds_data = {
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                'scopes': creds.scopes,
                'expiry': creds.expiry.isoformat() if creds.expiry else None
            }
            
            with open('token.json', 'w') as token_file:
                json.dump(creds_data, token_file, indent=2)
            
            return creds
            
        except FileNotFoundError:
            print("❌ Error: credentials.json not found!")
            print("Please download your OAuth client credentials from Google Cloud Console")
            print("and save them as 'credentials.json' in this directory.")
            return None
        except Exception as e:
            print(f"❌ Authorization failed: {e}")
            return None
    
    @staticmethod
    def _save_credentials(creds):
        """ Saves updated credentials back to token.json """
        creds_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes,
            'expiry': creds.expiry.isoformat() if creds.expiry else None
        }
        with open('token.json', 'w') as token_file:
            json.dump(creds_data, token_file, indent=2)

    @staticmethod
    def get_emails_last_24_hours():
        """ Gets all messages sent in the past 24 hoursw """
        # Get the service
        service = GmailPipe.get_gmail_service()

        # Get current time and the time 24 hours ago
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        query = f"after:{int(yesterday.timestamp())}"

        # Get message info from the past 24 hours
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        email_list = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            headers = msg_data['payload']['headers']
            payload = msg_data['payload']

            # Helper method for retrieving headers
            def get_header(name):
                """ Retrieves the specified header """
                return next((h['value'] for h in headers if h['name'].lower() == name.lower()), None)
            
            # Get the first 3 fields
            subject = get_header('Subject') or "(No Subject)"
            sender = get_header('From') or "(Unknown Sender)"
            date = get_header('Date')
            
            # Get email body (the 4th field)
            parts = msg_data['payload'].get('parts', [])
            if parts:
                for part in parts:
                    if part.get('mimeType') == 'text/plain':
                        body_data = part['body']['data']
                        body = base64.urlsafe_b64decode(body_data.encode('UTF-8')).decode('UTF-8')
                        break
            else:
                body_data = msg_data['payload']['body'].get('data')
                if body_data:
                    body = base64.urlsafe_b64decode(body_data.encode('UTF-8')).decode('UTF-8')

            email = Email(subject, sender, date, body) # Create an email object
            email_list.append(email) # add it to the list

        return email_list
