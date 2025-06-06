# Data utility class for storing emails
# @author Rylan Ahmadi (Ry305)
# Last updated 06/06/2025

from googleapiclient.discovery import build
import base64
from myEmail import Email
from datetime import datetime, timedelta

class GmailPipe: 

    def get_gmail_service():
        """ Creates and returns a service for the gmail API (assumes credentials have already been
        set up). """
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.readonly'])
        service = build('gmail', 'v1', credentials=creds)
        return service

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
