import streamlit as st
from modules.nav import SideBarLinks
import requests
import os
from datetime import datetime

from modules.config import get_api_base_url

API_BASE_URL = get_api_base_url()

# response = requests.get(f"{API_BASE_URL}/c/clubs")



SideBarLinks()

st.title(f"Welcome {st.session_state.first_name}!")

# ----------------- Show all clubs in a dropdown -----------------
st.subheader("Available Clubs")
response = requests.get(f"{API_BASE_URL}/c/clubs")
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
            "recipient_id": 0,  
            "recipient_type": "system",  
            "sender_id": st.session_state.get("nuid", 1),
            "sender_type": "student",
            "content": content
        }


st.title("My Club/Event Applications")

# -------------------- Student Applications --------------------
st.subheader("My Club/Event Applications")

applicant_id = st.text_input("Enter your Applicant ID to see your applications", placeholder="e.g. 83")

if applicant_id:
    try:
        int_id = int(applicant_id)
        url = f"http://api:4000/applications?applicant_id={int_id}"
        response = requests.get(url)

        if response.status_code == 200:
            applications = response.json()
            if applications:
                st.write("### Your Applications")
                for app in applications:
                    st.markdown(f"""
                     **Application ID**: `{app['id']}`  
                     **Club ID**: `{app['club_id']}`  
                     *Status**: `{app['status'].capitalize()}`
                    ---
                    """)
            else:
                st.info("No applications found for this Applicant ID.")
        else:
            st.error("Error fetching applications.")
    except ValueError:
        st.error("Applicant ID must be a number.")

# -------------------- For commments --------------------
st.subheader("Check Out Comments on a Club")

nuid = st.text_input("Please enter your NUID to view your comments:")

if nuid:
    response = requests.get(f"http://api:4000/comments?nuid={nuid}")
    if response.status_code == 200:
        comments = response.json()
        for c in comments:
            st.markdown(f"- 🗨️ {c['text']} *(Posted on {c['date']})*")


# -------------------- Personalized Club Recommendations --------------------
st.subheader("🎯 Recommended Clubs Based on Your Interests")

# Use the currently logged-in user's NUID
applicant_id = st.session_state.get("nuid")

if applicant_id:
    try:
        response = requests.get(f"http://api:4000/recommend/recommendations?applicant_id={applicant_id}")
        if response.status_code == 200:
            recommendations = response.json()
            if recommendations:
                for rec in recommendations:
                    st.markdown(f"🎯 **{rec['name']}** - {rec['type']} | {rec['subject']}")
            else:
                st.info("No relevant clubs or events found at this time.")
        else:
            st.error("Could not fetch recommendations.")
    except Exception as e:
        st.error(f"Error fetching recommendations: {e}")
else:
    st.warning("You must be logged in to see recommendations.")

