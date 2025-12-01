
#in PS
#.\venv\Scripts\activate
#CMD
#venv\Scripts\activate
#streamlit run app.py


import streamlit as st
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
    return [e.strip() for e in email_str.split(",") if e.strip()]


if submitted:
    if not to_email or not subject or not message:
        st.error("❗ To, Subject, and Message are required.")
    else:
        try:
            to_list = clean_email_list(to_email)
            cc_list = clean_email_list(cc_email)
            bcc_list = clean_email_list(bcc_email)

            # Save uploaded attachments temporarily
            saved_files = []
            if attachments:
                for file in attachments:
                    path = f"/tmp/{file.name}"
                    with open(path, "wb") as f:
                        f.write(file.read())
                    saved_files.append(path)

            # Send email
            success = send_gmail_message(
                to_list,
                cc_list,
                bcc_list,
                subject,
                message,
                attachments=saved_files
            )

            if success:
                st.success("✅ Email sent successfully!")
            else:
                st.error("❗ Email failed to send. Check .env settings or server logs.")

        except Exception as e:
            st.error(f"❌ Error sending email: {e}")
