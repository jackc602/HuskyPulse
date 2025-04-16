import logging
import streamlit as st
import os
import requests
from datetime import datetime
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
SideBarLinks()

current_file = os.path.abspath(__file__)
logger.info(f"cwd returns: {os.getcwd()} , current file returns {current_file}")
src_dir = os.path.dirname(os.path.dirname(current_file))
logger.info(os.getcwd())

st.title("Create New Event")

name = st.text_input("Event Name:")
id = st.number_input("Event ID", min_value=1, step=1)
start_date = st.date_input("Start Date:")
start_time = st.time_input("Start Time:")
end_date = st.date_input("End Date:")
end_time = st.time_input("End Time:")

location_id = st.number_input("Location ID", min_value=1, step=1)

if st.button("Create Event"):
    if not name:
        st.error("Event must have a name.")
    else:
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)

        event_data = {
            "id": id,
            "name": name,
            "start_date": start_datetime.isoformat(),
            "end_date": end_datetime.isoformat(),
            "location_id": location_id,
            "club_id": st.session_state.club_id
        }

        try:
            response = requests.post("http://api:4000/event/event", json=event_data)
            if response.status_code == 200:
                st.success("Event created successfully!")
                logger.info(f"Event added with data {event_data}")
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error creating event. {e}")

if st.button("Back"):
    st.switch_page("pages/page01_club_home.py")
