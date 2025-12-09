import streamlit as st
import pandas as pd
from email_service1 import send_gmail_message

st.set_page_config(page_title="Simple Mail Merge", layout="centered")
st.title("📧 Simple Mail Merge Email Sender")

# -------------------------
# Session State Setup
# -------------------------
if "records" not in st.session_state:
    st.session_state.records = []

if "index" not in st.session_state:
    st.session_state.index = 0

if "template" not in st.session_state:
    st.session_state.template = ""


# -------------------------
# File Upload Section
# -------------------------
st.header("1️⃣ Upload Template & CSV")

template_file = st.file_uploader("Upload template (.txt)", type=["txt"])
csv_file = st.file_uploader("Upload CSV (.csv)", type=["csv"])

if template_file:
    st.session_state.template = template_file.read().decode("utf-8")

if csv_file:
    df = pd.read_csv(csv_file)
    st.session_state.records = df.to_dict("records")

# Stop if files missing
if not st.session_state.template or not st.session_state.records:
    st.warning("Please upload both template.txt and CSV file to continue.")
    st.stop()


# -------------------------
# Prepare Current Record
# -------------------------
idx = st.session_state.index
total = len(st.session_state.records)
record = st.session_state.records[idx]

# Merge template with CSV row
try:
    merged_message = st.session_state.template.format(**record)
except Exception as e:
    st.error(f"Template error: {e}")
    st.stop()

st.header("2️⃣ Review & Send Email")
st.info(f"Record {idx + 1} of {total}")


# -------------------------
# Email Form
# -------------------------
with st.form("email_form"):
    to_email = st.text_input("Email", value=record.get("email", ""))
    subject = st.text_input("Subject", value="Your Mail Merge Message")
    message = st.text_area("Message", value=merged_message, height=180)

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        back_btn = st.form_submit_button("⬅ Back")
    with col2:
        next_btn = st.form_submit_button("Next ➡")
    with col3:
        send_btn = st.form_submit_button("📨 Send")


# -------------------------
# Navigation Buttons
# -------------------------
if back_btn:
    if st.session_state.index > 0:
        st.session_state.index -= 1
    st.rerun()


if next_btn:
    if st.session_state.index < total - 1:
        st.session_state.index += 1
    st.rerun()



# -------------------------
# Send Email
# -------------------------
if send_btn:
    ok = send_gmail_message([to_email], [], [], subject, message, attachments=None)
    if ok:
        st.success("✅ Email sent successfully!")
    else:
        st.error("❗ Failed to send email.")


st.markdown("---")
st.caption("Simple Mail Merge using Gmail SMTP + Streamlit © 2025")
