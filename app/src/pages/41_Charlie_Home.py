import os
import sys

# Add the modules folder to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))

import streamlit as st
from nav import SideBarLinks

# Set page config
st.set_page_config(layout='wide')

SideBarLinks()

# Main content
st.title(f"Welcome Student, {st.session_state['first_name']}.")

st.write("This is your student dashboard. Here you can:")
st.markdown("- 📄 View posts from clubs")
st.markdown("- 📝 Apply to events")
st.markdown("- 📊 Track your activity and engagement")

if st.button("Go Back to Home"):
    st.switch_page("Home.py")
