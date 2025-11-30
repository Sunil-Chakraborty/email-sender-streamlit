import streamlit as st
from email_service import send_gmail_message

st.set_page_config(page_title="Gmail API Email Sender", page_icon="📧", layout="centered")

st.title("📧 Send Email via Gmail API")
st.write("Use this simple Streamlit interface to send email securely using the Gmail API.")

with st.form("email_form"):
    to_email = st.text_input("Recipient Email", placeholder="example@domain.com")
    subject = st.text_input("Subject", placeholder="Enter your subject")
    message = st.text_area("Message", height=200, placeholder="Type your message here...")

    submitted = st.form_submit_button("Send Email")

if submitted:
    if not to_email or not subject or not message:
        st.error("❗ All fields are required to send the email.")
    else:
        try:
            result = send_gmail_message(to_email, subject, message)
            if result:
                st.success("✅ Email sent successfully!")
            else:
                st.error("❗ Failed to send email. Check logs for details.")
        except Exception as e:
            st.error(f"Error: {e}")
