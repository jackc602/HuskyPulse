import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
from datetime import datetime as dt

SideBarLinks()

specifier = {"event_id": st.session_state.event_to_edit}
response = requests.get("http://api:4000/event", params = specifier)
event_data = response.json()[0]

st.title("Edit Event")
st.write(event_data)

name = st.text_input("Name:", value = event_data["name"])

start_date = st.date_input("Start Date:")
start_time = st.time_input("Start Time:")
end_date = st.date_input("End Date:")
end_time = st.time_input("End Time:")

locations = pd.DataFrame(requests.get("http://api:4000/location/location").json())

building_options = locations["building"].unique()
building = st.selectbox("Building", options = building_options)

room_options = locations[locations["building"] == building]["room_num"]
room = st.selectbox("Room Number", options = room_options)

if st.button("Save Changes"):
    if not name:
        st.error("Event must have a name.")
    else:
        start_datetime = dt.combine(start_date, start_time)
        end_datetime = dt.combine(end_date, end_time)
        
        building = locations[locations["building"] == building]
        loc_id = building[building["room_num"] == room]["id"].iloc[0]

        event_data = {
            "name": name,
            "start_date": start_datetime.isoformat(),
            "end_date": end_datetime.isoformat(),
            "location_id": int(loc_id),
            "event_id": st.session_state.event_to_edit
        }
        try:
            response = requests.post("http://api:4000/event/update", json = event_data)
            st.success("Event edited Successfully!")
            logger.info(f"Event {event_data['event_id']} was updated")
        except Exception as e:
            st.error(f"Error editing event. {e}")

if st.button("Back"):
    st.switch_page("pages/page06_view_event_club.py")