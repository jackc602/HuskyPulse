import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks


# Configure the page
st.set_page_config(
    page_title="Student_Events",
    layout="wide"
)


SideBarLinks()

nuid = st.session_state.get("nuid")

if nuid:
    try:
        response = requests.get("http://api:4000/rsvp")
        if response.status_code == 200:
            rsvps = response.json()
            filtered = [r for r in rsvps if str(r['NUID']) == str(nuid)]
            if filtered:
                st.subheader("These are the Events that you have RSVPD for, along with some specific details of each event")
                df = pd.DataFrame(filtered)
                df.rename(columns={
                    "name": "Event Name",
                    "when_rsvped": "RSVP Time",
                    "start_date": "Start Date",
                    "end_date": "End Date",
                    "location_id": "Location ID"
                 }
                 , inplace=True)
                st.dataframe(df)
            else:
                st.info("You haven't RSVPed to any events yet.")

        else:
            st.error("Failed to fetch RSVP data.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.warning("You must me logged in or have a valid NUid to continue")




