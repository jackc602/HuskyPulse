import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title("View your Existing Applications")


if st.button("Back"):
    st.switch_page("pages/page12_application_student.py")