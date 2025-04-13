import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

SideBarLinks()

st.title(f"Welcome {st.session_state.first_name}!")

# ----------------- Show all clubs in a dropdown -----------------
st.subheader("Available Clubs")
response = requests.get("http://web-api:4000/club/clubs")
if response.status_code == 200:
    clubs = response.json()
    
    # List of club names in the dropdown 
    club_options = [f"{club['name']} - {club['type']} | {club['subject']}" for club in clubs]

    # Show dropdown and capture selection
    selected_club = st.selectbox("Select a club!:", club_options)

# ----------------- Submit Feedback -----------------
st.subheader("Submit Feedback for HuskyPulse")

with st.form("feedback_form"):
    content = st.text_area("What would you like to share about HuskyPulse? We would love to hear so we can make this app better for everyone!")
    submitted = st.form_submit_button("Submit Feedback")

    if submitted and content.strip():
        feedback_data = {
            "recipient_id": 0,  # or 1 if needed — since it's HuskyPulse, pick a consistent ID
            "recipient_type": "system",  # or "admin", whatever your backend expects
            "sender_id": st.session_state.get("nuid", 1),
            "sender_type": "student",
            "content": content
        }


