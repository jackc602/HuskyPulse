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
    
    # Create a list of club names for the dropdown
    club_options = [f"{club['name']} - {club['type']} | {club['subject']}" for club in clubs]

    # Show dropdown and capture selection
    selected_club = st.selectbox("Select a club to learn more:", club_options)

