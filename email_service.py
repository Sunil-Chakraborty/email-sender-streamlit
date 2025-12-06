import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Read variables from your existing .env file
EMAIL_HOST = os.getenv("EMAIL_HOST")                 # smtp.gmail.com
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))       # 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")       # Gmail address
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # App password
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"


def send_gmail_message(to_emails, cc_emails, bcc_emails, subject, body, attachments=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_HOST_USER
        msg["To"] = ", ".join(to_emails)
        msg["Cc"] = ", ".join(cc_emails)
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Attach files
        if attachments:
            for file_path in attachments:
                try:
                    part = MIMEBase("application", "octet-stream")
                    with open(file_path, "rb") as f:
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={os.path.basename(file_path)}"
                    )
                    msg.attach(part)
                except Exception as e:
                    print("Attachment error:", e)

        # Combine recipients
        all_recipients = list(set(to_emails + cc_emails + bcc_emails))

        # Debug info
        print("\n--- DEBUG INFO ---")
        print("SMTP Server:", EMAIL_HOST)
        print("SMTP Port:", EMAIL_PORT)
        print("Login User:", EMAIL_HOST_USER)
        print("To:", to_emails)
        print("CC:", cc_emails)
        print("BCC:", bcc_emails)
        print("Total recipients:", all_recipients)
        print("------------------\n")

        # Connect SMTP
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            if EMAIL_USE_TLS:
                server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_HOST_USER, all_recipients, msg.as_string())

        return True

    except Exception as e:
        print("Email sending failed:", e)
        return False
