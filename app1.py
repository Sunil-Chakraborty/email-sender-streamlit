import streamlit as st
from email_service import send_gmail_message

# --------------------------
# Streamlit Page Settings
# --------------------------
st.set_page_config(
    page_title="Gmail Email Sender",
    page_icon="📧",
    layout="centered"
)

# --------------------------
# Page Title
# --------------------------
st.title("📧 Gmail SMTP Email Sender")
st.write("Send emails securely using your Gmail App Password.")

st.markdown("---")

# --------------------------
# Email Form
# --------------------------
with st.form("email_form"):
    to_email = st.text_input(
        "Recipient Email",
        placeholder="example@domain.com"
    )

    subject = st.text_input(
        "Subject",
        placeholder="Enter your subject..."
    )

    message = st.text_area(
        "Message",
        height=200,
        placeholder="Type your message here..."
    )

    submitted = st.form_submit_button("📨 Send Email")

# --------------------------
# Form Submission Handling
# --------------------------
if submitted:
    if not to_email or not subject or not message:
        st.error("❗ All fields are required.")
    else:
        try:
            email_sent = send_gmail_message(to_email, subject, message)

            if email_sent:
                st.success("✅ Email sent successfully!")
            else:
                st.error("❗ Email failed to send. Check server logs or .env settings.")

        except Exception as e:
            st.error(f"❌ Error sending email: {e}")

st.markdown("---")
st.caption("Powered by Gmail SMTP + Streamlit © 2025")
