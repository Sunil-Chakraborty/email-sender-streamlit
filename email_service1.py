import smtplib
from email.mime.text import MIMEText
import settings


def send_gmail_message(to_email, subject, message):
    try:
        # Construct the email
        msg = MIMEText(message, "plain")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_HOST_USER
        msg["To"] = to_email

        print("SMTP Server:", EMAIL_HOST)
        print("SMTP Port:", EMAIL_PORT)
        print("Login User:", EMAIL_HOST_USER)
        print("To:", to_email)
        
        
        print("------------------\n")
        
        # Connect to Gmail SMTP Server
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            # Send email
            server.sendmail(settings.EMAIL_HOST_USER, to_email, msg.as_string())

        # IMPORTANT: Must return True for success
        return True

    except Exception as e:
        print("Email sending failed:", e)
        return False
