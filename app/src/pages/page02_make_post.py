
import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Make a New Post")

if st.button("Back"):
    st.switch_page("pages/page01_club_home.py")