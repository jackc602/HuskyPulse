import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("View Applications")

# Get current student's NUID from session
nuid = st.session_state.get("nuid")

if nuid:
    try:
        # calling the backend API so that I can extract out a certain post from a student using their NUID
        response = requests.get(f"http://api:4000/applications?applicant_id={nuid}")
        
        if response.status_code == 200:
            applications = response.json()
            
            if applications:
                st.subheader("Here are your applications:")
                for application in applications:
                    st.markdown(f"### {application['club_name']}")
                    st.write("Status:", application['status'])

                
            else:
                st.info("No applications available yet.")
        else:
            st.error("Could not fetch applications.")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("You must be logged in to see applications.")

