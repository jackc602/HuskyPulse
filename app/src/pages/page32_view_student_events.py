import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(page_title="Student RSVPs", layout="centered")
SideBarLinks()


st.title("Events")

# Function to fetch all student RSVP data
def fetch_events():
    try:
        res = requests.get("http://api:4000/student_event/all_event_rsvps")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error("Failed to fetch student RSVP data.")
        st.error(e)
        return []

# Fetch data and show in table
events = fetch_events()

for event in events:
    st.subheader(event["event_name"])

    st.markdown(f"""
    **Start Date:** {event['start_date']}  
    **End Date:** {event['end_date']}  
    **Building:** {event['building']}  
    **Room Number:** {event['room_num']}  
    """)

    nuid = st.session_state.get("nuid")

    specifier = {"event_id": event["id"]}
    response = requests.get("http://api:4000/rsvp/event", params=specifier)
    response.raise_for_status()
    event_rsvps = pd.DataFrame(response.json())

    if event_rsvps.empty:
        st.info("No RSVPs yet.")
    else:
        st.markdown(f"**RSVP Count:** {len(event_rsvps)}")
        st.table(event_rsvps[["email", "first_name", "last_name", "when_rsvped"]])

    # RSVP Button
    if st.button(f"RSVP to {event['event_name']}", key=f"rsvp-{event['id']}"):
        # try:
        res = requests.post(
            "http://api:4000/rsvp/insert_rsvp",
            json={
                "event_id": event["id"],
                "NUID": nuid
            }
        )
        if res.status_code == 200:
            st.success(f"You RSVPed to {event['event_name']}!")
        else:
            st.write(res.status_code)
            st.warning("RSVP failed.")


    st.markdown("---")  
 



   