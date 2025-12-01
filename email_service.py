import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("SMTP_SERVER")
EMAIL_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_HOST_USER = os.getenv("SMTP_EMAIL")
EMAIL_HOST_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_gmail_message(to_emails, cc_emails, bcc_emails, subject, body, attachments=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_HOST_USER
        msg["To"] = ", ".join(to_emails)
        msg["Cc"] = ", ".join(cc_emails)
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # 🗂 Add attachments (if any)
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

        # Combine all recipients for sending
        all_recipients = list(set(to_emails + cc_emails + bcc_emails))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_HOST_USER, all_recipients, msg.as_string())

        return True

    except Exception as e:
        print("Email sending failed:", e)
        return False
