import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.write(st.session_state["post_to_edit"])

if st.button("Back"):
    st.switch_page("pages/page03_view_post_club.py")