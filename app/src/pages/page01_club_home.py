
import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Hawaii Club Home Page")

if st.button("Make a new post"):
    st.switch_page("pages/page02_make_post.py")