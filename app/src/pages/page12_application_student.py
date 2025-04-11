import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Applications Page")

if st.button("Make an Application", key = "apply"):
    st.switch_page("pages/page13_apply_student.py")

if st.button("View your Applications", key = "view"):
    st.switch_page("pages/page14_view_applications_student.py")