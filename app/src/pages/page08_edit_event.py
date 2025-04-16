import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import os
import uuid
from modules.nav import SideBarLinks

SideBarLinks()

specifier = {"event_id": st.session_state.event_to_edit}
response = requests.get("http://api:4000/event", params = specifier)
event_data = response.json()[0]

st.title("Edit Event")
st.write(event_data)



if st.button("Back"):
    st.switch_page("pages/page06_view_event_club.py")