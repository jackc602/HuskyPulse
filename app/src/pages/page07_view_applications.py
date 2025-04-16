# Streamlit Page
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()


st.title("Manage Applications")

# Get club ID from session
club_id = st.session_state.club_id

if club_id is None:
    st.error("No club ID found in session.")
else:
    # Fetch applications from backend
    response = requests.get(f"http://api:4000/application/club/{club_id}")
    
    if response.status_code == 200:
        applications = response.json()
        
        if not applications:
            st.info("No applications for this club.")
        else:
            for app in applications:
                st.subheader(f"Application ID: {app['id']} (Applicant ID: {app['applicant_id']})")
                st.write(f"Name: {app['first_name']} {app['last_name']}")
                st.write(f'Current Status: {app["status"]}')
                
                new_status = st.selectbox(
                    "Status",
                    ["accepted", "in progress", "rejected"],
                    index=["accepted", "in progress", "rejected"].index(app["status"]),
                    key=f"status_{app['id']}"
                )
                
                if st.button("Update Status", key=f"btn_{app['id']}"):
                    payload = {
                        "status": new_status,
                        "id": app["id"],
                        "club_id": club_id,
                        "applicant_id": app["applicant_id"]
                    }
                    update_response = requests.put(
                        f"http://web-api:4000/application/update",
                        json=payload
                    )
                    if update_response.status_code == 200:
                        st.success(f"Application {app['id']} updated!")
                    else:
                        st.error(f"Failed to update application {app['id']}")
    else:
        st.error("Failed to fetch applications.")
