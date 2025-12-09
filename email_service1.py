import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# PDF generation imports
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# -------------------------------------------------------
# Load .env reliably from same directory
# -------------------------------------------------------


# Load .env
load_dotenv()

# Use  existing .env variable names
EMAIL_HOST = os.getenv("EMAIL_HOST")                     # smtp.gmail.com
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))           # 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")           # Gmail address
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")   # App password
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"


# -------------------------------------------------------
# Function: Create a PDF Summary File
# -------------------------------------------------------
def create_pdf_summary(recipient, subject, message, pdf_path):
    """
    Creates a simple PDF summary using reportlab.
    """
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    text = c.beginText(40, height - 50)
    text.setFont("Helvetica", 11)

    lines = [
        f"Email Summary",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Recipient: {recipient}",
        f"Subject: {subject}",
        "",
        "Message Body:",
        "----------------------------"
    ]

    # Add summary header text
    for line in lines:
        text.textLine(line)

    # Add message body (multi-line support)
    for line in message.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()


# -------------------------------------------------------
# Function: Send Email (HTML + Attachments + PDF Summary)
# -------------------------------------------------------
def send_gmail_message(to_emails, cc_emails, bcc_emails,
                       subject, body, is_html=False,
                       attachments=None,
                       generate_pdf=False):
    """
    Send an email using Gmail SMTP with:
    - HTML or plain text
    - Attachments
    - Optional PDF summary file
    """

    try:
        # ------------------------------
        # Build email
        # ------------------------------
        msg = MIMEMultipart()
        msg["From"] = EMAIL_HOST_USER
        msg["To"] = ", ".join(to_emails)
        msg["Cc"] = ", ".join(cc_emails)
        msg["Subject"] = subject

        # Attach message body
        if is_html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))

        # ------------------------------
        # Add PDF summary if requested
        # ------------------------------
        if generate_pdf:
            pdf_path = f"/tmp/email_summary_{to_emails[0]}.pdf"
            create_pdf_summary(to_emails[0], subject, body, pdf_path)

            part = MIMEBase("application", "octet-stream")
            with open(pdf_path, "rb") as f:
                part.set_payload(f.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename=summary_{to_emails[0]}.pdf"
            )
            msg.attach(part)

        # ------------------------------
        # Attach uploaded files
        # ------------------------------
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

        # ------------------------------
        # Final recipient list
        # ------------------------------
        all_recipients = list(set(to_emails + cc_emails + bcc_emails))

        # ------------------------------
        # Send Email via Gmail SMTP
        # ------------------------------
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()                     # REQUIRED
            server.starttls()                 # Secure TLS
            server.ehlo()                     # REQUIRED again after TLS
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_HOST_USER, all_recipients, msg.as_string())
            
        print("DEBUG ENV:", EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        
        print("Email successfully sent to:", all_recipients)
        return True

    except Exception as e:
        print("DEBUG SMTP:", EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER)

        print("Email sending FAILED:", e)
        return False
