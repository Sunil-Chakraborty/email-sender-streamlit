# email_service.py
import smtplib
from email.mime.text import MIMEText
import settings

def send_email(to, subject, message):
    # 1. Create email object
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = to

    # 2. Connect to Gmail server
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()

    # 3. LOGIN happens here
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # 4. Send email
    server.send_message(msg)

    # 5. Close
    server.quit()
