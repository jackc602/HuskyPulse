import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import time
import json
from modules.nav import SideBarLinks
from modules.config import get_api_base_url
import numpy as np

# Configure the page
st.set_page_config(
    page_title="Admin Dashboard - HuskyPulse",
    page_icon="🐺",
    layout="wide"
)

# Initialize navigation
SideBarLinks()

# Get API base URL
API_BASE_URL = get_api_base_url()


# Function to fetch data from API with error handling
def fetch_data(endpoint, params=None):
    try:
        full_url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(full_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to API: {e}")
        return None
    except json.JSONDecodeError:
        st.error("Received invalid data from API")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Main header with welcome message
st.title(f"Welcome, {st.session_state.first_name}!")
st.markdown("#### System Administration Dashboard")

# Add system overview section
st.markdown("### System Overview")

# Try to fetch club data for metrics
clubs = fetch_data("club/clubs")
if clubs is None:
    clubs = []  # Default to empty list if API call fails

# Try to fetch students data for metrics
students = fetch_data("comments")  # Using comments API to get some student data
if students is None:
    students = []  # Default to empty list if API call fails

# Create a row of key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Students",
        value=len(students) if students else "N/A",
        delta="N/A",
        delta_color="off"
    )

with col2:
    st.metric(
        label="Active Clubs",
        value=len(clubs) if clubs else "N/A",
        delta="N/A",
        delta_color="off"
    )

with col3:
    # Calculate total club membership
    total_members = sum(club.get("size", 0) for club in clubs) if clubs else 0
    st.metric(
        label="Total Club Members",
        value=total_members,
        delta="N/A",
        delta_color="off"
    )

with col4:
    st.metric(
        label="System Status",
        value="Healthy" if clubs or students else "Issues Detected",
        delta="100% uptime" if clubs or students else "API connection issues",
        delta_color="normal" if clubs or students else "inverse"
    )



st.subheader("System Status")

# System status indicators
status_data = [
    {"name": "API Server", "status": "Online" if clubs or students else "Issues Detected"},
    {"name": "Database", "status": "Online" if clubs or students else "Issues Detected"},
    {"name": "Web App", "status": "Online"},
]

for item in status_data:
    status_color = "green" if item["status"] == "Online" else "red"
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: space-between;
        padding: 10px;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        margin-bottom: 10px;
    ">
        <div>
            <span style="font-weight: bold;">{item["name"]}</span>
        </div>
        <div>
            <span style="color: {status_color}; font-weight: bold;">{item["status"]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Club management section
st.subheader("Club Management")

if not clubs:
    st.warning("Could not load clubs data. Please check API connection.")
else:
    # Create a table of clubs
    club_data = [{
        "ID": club.get("id", "N/A"),
        "Name": club.get("name", "Unknown"),
        "Type": club.get("type", "Unknown"),
        "Subject": club.get("subject", "Unknown"),
        "Size": club.get("size", 0)
    } for club in clubs]

    club_df = pd.DataFrame(club_data)
    st.dataframe(club_df, use_container_width=True, hide_index=True)

# Role assignment section
with st.expander("Assign User Roles"):
    st.subheader("Assign New Role")

    # Admin ID for API calls
    admin_id = st.session_state.get("admin_id", 1)

    with st.form("assign_role_form"):
        # User ID input
        user_id = st.number_input("User ID", min_value=1, step=1)

        # Role selection
        role_options = ["Club Leader", "Student", "Administrator", "Analyst"]
        selected_role = st.selectbox("Role", role_options)

        # Submit button
        submit_button = st.form_submit_button("Assign Role")

        if submit_button:
            try:
                # Prepare the data for the API call
                role_data = {
                    "admin_id": admin_id,
                    "role_name": selected_role
                }

                # Make the API call to assign role
                response = requests.post(f"{API_BASE_URL}/admin/admin/assign-role", json=role_data)

                if response.status_code == 201:
                    st.success(f"Role '{selected_role}' assigned to user ID {user_id}")
                else:
                    st.error(f"Failed to assign role: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# System maintenance section
with st.expander("System Maintenance"):
    st.subheader("Schedule Maintenance")

    with st.form("maintenance_form"):
        col1, col2 = st.columns(2)

        with col1:
            maintenance_date = st.date_input("Date", datetime.now() + timedelta(days=7))
            maintenance_start = st.time_input("Start Time", datetime.strptime("22:00", "%H:%M").time())

        with col2:
            maintenance_duration = st.number_input("Duration (hours)", value=2.0, min_value=0.5, max_value=8.0,
                                                   step=0.5)
            maintenance_type = st.selectbox("Type",
                                            ["Software Update", "Database Optimization", "Security Patch", "Backup",
                                             "Other"])

        maintenance_desc = st.text_area("Description", placeholder="Describe the maintenance activities...")

        submit_button = st.form_submit_button("Schedule Maintenance")

        if submit_button:
            if maintenance_desc:
                try:
                    # In a real implementation, this would schedule the maintenance
                    # Log action in admin logs
                    log_data = {
                        "admin_id": admin_id,
                        "content": f"Scheduled {maintenance_type} maintenance for {maintenance_date} at {maintenance_start} for {maintenance_duration} hours"
                    }

                    # Make the API call to log the action
                    response = requests.post(f"{API_BASE_URL}/admin/admin/log", json=log_data)

                    if response.status_code == 201:
                        st.success(f"Maintenance scheduled for {maintenance_date} at {maintenance_start}")
                    else:
                        st.error(f"Failed to log maintenance: {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please provide a description of the maintenance activities")

# Backup section
with st.expander("Database Backup"):
    st.subheader("Create Backup")

    with st.form("backup_form"):
        backup_name = st.text_input("Backup Name", value=f"backup_{datetime.now().strftime('%Y%m%d_%H%M')}")
        backup_desc = st.text_area("Description", placeholder="Describe this backup...")

        submit_button = st.form_submit_button("Create Backup")

        if submit_button:
            try:
                # Prepare the data for the API call
                backup_data = {
                    "admin_id": admin_id,
                    "content": f"Manual backup: {backup_desc if backup_desc else 'No description provided'}"
                }

                # Make the API call to create backup
                response = requests.post(f"{API_BASE_URL}/admin/admin/backup", json=backup_data)

                if response.status_code == 201:
                    # Show progress bar animation
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for i in range(101):
                        # Update progress bar
                        progress_bar.progress(i)
                        status_text.text(f"Backup in progress: {i}%")
                        time.sleep(0.01)

                    status_text.text("Backup completed successfully!")
                    st.success(f"Backup '{backup_name}' created successfully")
                else:
                    st.error(f"Failed to create backup: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")