import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))

from nav import SideBarLinks
import logging
import streamlit as st
from nav import SideBarLinks


st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome Club Leader, {st.session_state['first_name']}.")
st.write('')
st.write('')

if st.button("Go Back to Home"):
    st.switch_page("00_Pol_Strat_Home.py")
