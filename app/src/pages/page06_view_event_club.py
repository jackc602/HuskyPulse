import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

SideBarLinks()

st.title("Event History")

specifier = {"club_id": st.session_state.club_id}
response = requests.get("http://api:4000/event/club", params = specifier)
response.raise_for_status()
event_data = response.json()

for event in event_data:
    st.subheader(event["name"])
    start = event["start_date"]
    end = event["end_date"].split()
    end_time = end[-2] + end[-1]
    st.write(start + " to " + end_time)
    st.write("**Location**")
    st.write(event["building"] + ", Room " + str(event["room_num"]))
    # fetch and display the rsvps to the event
    specifier = {"event_id": event["id"]}
    response = requests.get("http://api:4000/rsvp/event", params = specifier)
    response.raise_for_status()
    event_rsvps = pd.DataFrame(response.json())
    if event_rsvps.empty:
        st.write("No RSVPs yet")
    else:
        st.write("**RSVPs**    Count:", event_rsvps.shape[0])
        st.dataframe(data = event_rsvps, hide_index = True)

    if st.button("Edit Event", key = event["id"]):
        st.session_state["event_to_edit"] = event["id"]
        st.switch_page("pages/page08_edit_event.py")
    st.divider()