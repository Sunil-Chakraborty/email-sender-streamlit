import streamlit as st
import os
import tempfile
from email_service import send_gmail_message

st.set_page_config(page_title="📧 Email Sender", layout="centered")

st.title("📧 Gmail SMTP Email Sender")

with st.form("email_form"):
    to_email = st.text_input("To (comma-separated emails)")
    cc_email = st.text_input("CC (comma-separated emails)", "")
    bcc_email = st.text_input("BCC (comma-separated emails)", "")
    subject = st.text_input("Subject")
    message = st.text_area("Message", height=150)

    attachments = st.file_uploader(
        "Attachments (optional)", accept_multiple_files=True
    )

    submitted = st.form_submit_button("Send Email")


def clean_email_list(email_str):
    if not email_str:
        return []
    return [
        e.strip()
        for e in email_str.split(",")
        if e.strip() and "@" in e and "." in e  # simple validation
    ]


if submitted:
    if not to_email or not subject or not message:
        st.error("❗ To, Subject, and Message are required.")
    else:
        try:
            to_list = clean_email_list(to_email)
            cc_list = clean_email_list(cc_email)
            bcc_list = clean_email_list(bcc_email)

            # Save attachments to temp files
            saved_files = []          # will store paths
            saved_names = []          # will store original names

            if attachments:
                for file in attachments:
                    suffix = os.path.splitext(file.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(file.read())
                        saved_files.append(tmp.name)
                        saved_names.append(file.name)

            # Bundle as pairs: (temp_path, original_name)
            attachment_pairs = list(zip(saved_files, saved_names))

            # Send email
            success = send_gmail_message(
                to_list,
                cc_list,
                bcc_list,
                subject,
                message,
                attachments=attachment_pairs
            )

            if success:
                st.success("✅ Email sent successfully!")
            else:
                st.error("❗ Email failed to send. Check SMTP settings or logs.")

        except Exception as e:
            st.error(f"❌ Error sending email: {e}")
