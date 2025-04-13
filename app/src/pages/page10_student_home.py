import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

SideBarLinks()

st.title(f"Welcome {st.session_state.first_name}!")

# ----------------- Show all clubs in a dropdown -----------------
st.subheader("Available Clubs")
response = requests.get("http://api:4000/club/clubs")
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

club_id_for_comments = st.text_input("Enter Club ID to see comments for the club or event:")

if club_id_for_comments:
    try:
        response = requests.get(f"http://api:4000/comments?club_id={int(club_id_for_comments)}")
        if response.status_code == 200:
            comments_data = response.json()
            if comments_data:
                for c in comments_data:
                    st.markdown(f"- 🗨️ {c['text']} *(Posted on {c['date']})*")
            else:
                st.info("No comments found for this club.")
        else:
            st.error("Failed to fetch comments.")
    except ValueError:
        st.error("Club ID must be a number.")

