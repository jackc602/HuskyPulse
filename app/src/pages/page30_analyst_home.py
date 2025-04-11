import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

st.title(f"Welcome {st.session_state.first_name}!")