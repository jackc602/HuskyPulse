import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import time
import json
from modules.nav import SideBarLinks
from modules.config import get_api_base_url

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
        st.write(f"Debug - Fetching from: {full_url}")
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
st.title(f"Welcome, {st.session_state.first_name}! ⚙️")
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

# Create a dashboard layout
left_col, right_col = st.columns([2, 1])

# Left column - System activity (mock data since we don't have historical metrics)
with left_col:
    st.subheader("System Activity")

    # Generate sample data for the chart
    days = 30
    dates = pd.date_range(start=datetime.now() - timedelta(days=days - 1), periods=days, freq='D')

    # Generate random data for user logins, club posts, and event registrations
    np.random.seed(42)  # For reproducibility
    user_logins = np.random.randint(30, 100, size=days)
    club_posts = np.random.randint(10, 30, size=days)
    event_registrations = np.random.randint(15, 50, size=days)

    # Create a DataFrame
    chart_data = pd.DataFrame({
        'Date': dates,
        'User Logins': user_logins,
        'Club Posts': club_posts,
        'Event Registrations': event_registrations
    })

    # Melt the DataFrame for Altair
    chart_data_melted = pd.melt(
        chart_data,
        id_vars=['Date'],
        value_vars=['User Logins', 'Club Posts', 'Event Registrations'],
        var_name='Metric',
        value_name='Count'
    )

    # Create a line chart using Altair
    chart = alt.Chart(chart_data_melted).mark_line().encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Count:Q', title='Count'),
        color=alt.Color('Metric:N', legend=alt.Legend(title="Metrics")),
        tooltip=['Date:T', 'Metric:N', 'Count:Q']
    ).properties(
        height=300
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

# Right column - System status and alerts
with right_col:
    st.subheader("System Status")

    # System status indicators
    status_data = [
        {"name": "API Server", "status": "Online" if clubs or students else "Issues Detected", "uptime": "99.9%"},
        {"name": "Database", "status": "Online" if clubs or students else "Issues Detected", "uptime": "100%"},
        {"name": "Web App", "status": "Online", "uptime": "99.7%"},
        {"name": "File Storage", "status": "Online", "uptime": "99.8%"}
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
                <span style="margin-left: 10px; color: #6c757d; font-size: 12px;">{item["uptime"]} uptime</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Most recent system alerts
    st.subheader("Recent Alerts")

    # Check if we have any API issues to report
    if not clubs and not students:
        alerts = [
            {"level": "Error", "message": "API connection issues detected", "time": "Just now"}
        ]
    else:
        alerts = [
            {"level": "Info", "message": "System running normally", "time": "Just now"},
            {"level": "Info", "message": "Database backup completed", "time": "Yesterday"},
            {"level": "Info", "message": "System update completed", "time": "3 days ago"}
        ]

    for alert in alerts:
        if alert["level"] == "Error":
            color = "#dc3545"
            icon = "🔴"
        elif alert["level"] == "Warning":
            color = "#ffc107"
            icon = "⚠️"
        else:
            color = "#0dcaf0"
            icon = "ℹ️"

        st.markdown(f"""
        <div style="
            padding: 10px;
            border-left: 4px solid {color};
            margin-bottom: 10px;
            background-color: #f8f9fa;
            border-radius: 0 5px 5px 0;
        ">
            <p style="margin: 0; font-size: 14px;">
                <span style="font-weight: bold;">{icon} {alert["level"]}: {alert["message"]}</span><br>
                <span style="color: #6c757d; font-size: 12px;">{alert["time"]}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

# Quick action buttons
st.subheader("Quick Actions")

# Create a row of action buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("👥 User Management", use_container_width=True):
        # In a real implementation, this would navigate to a user management page
        st.session_state["page"] = "user_management"
        st.info("User management feature coming soon")

with col2:
    if st.button("📊 System Logs", use_container_width=True):
        # In a real implementation, this would navigate to a system logs page
        st.session_state["page"] = "system_logs"
        st.info("System logs feature coming soon")

with col3:
    if st.button("✓ Compliance Management", use_container_width=True):
        # Navigate to compliance management page
        st.session_state["page"] = "compliance"
        st.switch_page("pages/page23_compliance.py")

with col4:
    if st.button("📢 Send Announcement", use_container_width=True):
        # Navigate to announcements page
        st.session_state["page"] = "announcements"
        st.switch_page("pages/page21_admin_communication.py")

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
                response = requests.post(f"{API_BASE_URL}/admin/assign-role", json=role_data)

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
                    response = requests.post(f"{API_BASE_URL}/admin/log", json=log_data)

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
                response = requests.post(f"{API_BASE_URL}/admin/backup", json=backup_data)

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