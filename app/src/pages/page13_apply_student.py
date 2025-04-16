import logging
import streamlit as st
import os
import requests
from datetime import datetime
from modules.nav import SideBarLinks
import pandas as pd

logger = logging.getLogger(__name__)
SideBarLinks()

current_file = os.path.abspath(__file__)
logger.info(f"cwd returns: {os.getcwd()} , current file returns {current_file}")
src_dir = os.path.dirname(os.path.dirname(current_file))
logger.info(os.getcwd())

st.title("Apply for a Club")


clubs = pd.DataFrame(requests.get("http://api:4000/club/clubs").json())
club_options = clubs["name"].unique()
club = st.selectbox("Club", options = club_options)

id = clubs.loc[clubs['name']==club, 'id'].values[0]


if st.button("Apply"):
    if not club:
        st.error("Choose a Club.")
    else:
        

        applicant_data = {
            "club_id": int(id),
            "status": "in progress",
            "applicant_id": st.session_state.nuid
        }


        try:
            response = requests.post("http://api:4000/application/apply", json=applicant_data)
            if response.status_code == 200:
                st.success("Application created successfully!")
                logger.info(f"Application added with data {applicant_data}")
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error creating application. {e}")

if st.button("Back"):
    st.switch_page("pages/page12_application_student.py")