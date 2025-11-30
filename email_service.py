import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)


def send_gmail_message(to_email: str, subject: str, message: str) -> bool:
    """
    Sends email using Gmail SMTP and App Password.
    Returns True on success, False on failure.
    """

    try:
        msg = MIMEText(message, "plain")
        msg["Subject"] = subject
        msg["From"] = DEFAULT_FROM_EMAIL
        msg["To"] = to_email

        # Gmail SMTP
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
