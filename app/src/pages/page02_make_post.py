
import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Make a New Post")
col1, col2 = st.columns(2)

with col1:
    st.text_input("Event Name:")

    st.text_area("Description:")

    st.date_input("Date")

    st.time_input("Time")

with col2:
    st.text_input("Location:") # Make this into a dropdown of locations 
    # needs fetch of all location names

    st.checkbox("Public?")

    st.checkbox("Collect RSVPs?")

    st.file_uploader("Cover Image")

if st.button("Upload Post"):
    pass
    # need to fetch and format all the data and slide it into a put route
    
if st.button("Back"):
    st.switch_page("pages/page01_club_home.py")