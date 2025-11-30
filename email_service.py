import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from settings import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REFRESH_TOKEN,
    GOOGLE_USER_EMAIL,
)

def get_gmail_service():
    creds = Credentials(
        None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
    )
    service = build("gmail", "v1", credentials=creds)
    return service

def send_gmail_message(to_email, subject, message_text):
    service = get_gmail_service()

    message = MIMEText(message_text)
    message["to"] = to_email
    message["from"] = GOOGLE_USER_EMAIL
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        sent_message = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw_message})
            .execute()
        )
        return sent_message
    except Exception as e:
        print("Gmail API Error:", e)
        return None
