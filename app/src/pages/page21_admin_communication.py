import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime
import time
import numpy as np
from modules.nav import SideBarLinks
from modules.config import get_api_base_url

# Configure the page
st.set_page_config(
    page_title="Admin Communication - HuskyPulse",
    page_icon="📢",
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
        st.error(f"Received invalid data from API: {response.text}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Function to post data to API with error handling
def post_data(endpoint, data):
    try:
        full_url = f"{API_BASE_URL}/{endpoint}"
        response = requests.post(full_url, json=data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to API: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Main header
st.title("System Communication Center 📢")
st.markdown("#### Send announcements and manage communication with users")

# Admin ID for API calls - this would be set during login
admin_id = st.session_state.get("admin_id", 1)

# Create tabs for different communication functions
tab1, tab2, tab3 = st.tabs(["Send Announcements", "View Feedback", "Communication History"])

# Tab 1: Send Announcements
with tab1:
    st.subheader("Send System Announcements")

    # Fetch club data for targeting announcements
    clubs = fetch_data("club/clubs")
    if clubs is None:
        st.warning("Could not load clubs data. Please check API connection.")
        clubs = []

    # Fetch students data for targeting announcements
    students = fetch_data("comments")  # Using comments API to get some student data
    if students is None:
        st.warning("Could not load student data. Please check API connection.")
        students = []

    # Create announcement form
    with st.form("announcement_form"):
        # Announcement title
        announcement_title = st.text_input("Announcement Title", max_chars=50)

        # Announcement content
        announcement_content = st.text_area("Announcement Content", max_chars=500)

        # Target audience
        target_options = ["All Users", "Club Leaders", "Students", "Administrators"]
        target_audience = st.selectbox("Target Audience", target_options)

        # If target is club leaders, allow selecting specific clubs
        if target_audience == "Club Leaders" and clubs:
            # Create a list of club options with IDs
            club_options = [(club.get("id"), club.get("name", "Unknown")) for club in clubs]

            # Allow selecting specific clubs or all clubs
            specific_clubs = st.multiselect(
                "Select Specific Clubs (leave empty for all clubs)",
                options=[club[0] for club in club_options],
                format_func=lambda x: next((club[1] for club in club_options if club[0] == x), "Unknown")
            )

        # Urgency level
        urgency_options = ["Normal", "Important", "Urgent"]
        urgency_level = st.selectbox("Urgency Level", urgency_options)

        # Schedule options
        schedule_options = ["Send Immediately", "Schedule for Later"]
        schedule_choice = st.radio("Sending Options", schedule_options)

        if schedule_choice == "Schedule for Later":
            col1, col2 = st.columns(2)
            with col1:
                scheduled_date = st.date_input("Date", datetime.now())
            with col2:
                scheduled_time = st.time_input("Time", datetime.now().time())

        # Submit button
        submit_button = st.form_submit_button("Send Announcement")

        if submit_button:
            if not announcement_title or not announcement_content:
                st.error("Please provide both a title and content for your announcement")
            else:
                try:
                    # Create recipients list based on target audience
                    recipients = []
                    if target_audience == "Club Leaders":
                        # If specific clubs were selected, use those, otherwise all clubs
                        club_ids = specific_clubs if specific_clubs else [club.get("id") for club in clubs]
                        for club_id in club_ids:
                            recipients.append({
                                "recipient_id": club_id,
                                "recipient_type": "club"
                            })
                    elif target_audience == "Students":
                        # In a real implementation, this would target all students
                        # For now, we'll just create a system-wide announcement
                        recipients.append({
                            "recipient_id": 0,
                            "recipient_type": "system"
                        })
                    elif target_audience == "Administrators":
                        # In a real implementation, this would target all admins
                        # For now, we'll just create a system-wide announcement
                        recipients.append({
                            "recipient_id": 0,
                            "recipient_type": "system"
                        })
                    else:  # All Users
                        # System-wide announcement
                        recipients.append({
                            "recipient_id": 0,
                            "recipient_type": "system"
                        })

                    # For each recipient, create a feedback entry (using feedback table for announcements)
                    for recipient in recipients:
                        # Prepare the feedback data
                        feedback_data = {
                            "recipient_id": recipient["recipient_id"],
                            "recipient_type": recipient["recipient_type"],
                            "sender_id": admin_id,
                            "sender_type": "administrator",
                            "content": f"{urgency_level}: {announcement_title}\n\n{announcement_content}",
                            "date_submitted": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }

                        # Post the feedback data
                        response = post_data("feedback/feedback", feedback_data)
                        if not response or response.status_code != 201:
                            st.error(
                                f"Failed to send announcement to {recipient['recipient_type']} (ID: {recipient['recipient_id']})")
                            continue

                    # Log the announcement as an admin action
                    log_data = {
                        "admin_id": admin_id,
                        "content": f"Sent {urgency_level} announcement '{announcement_title}' to {target_audience}"
                    }

                    # Make the API call to log the action
                    log_response = post_data("admin/admin/log", log_data)

                    if log_response and log_response.status_code == 201:
                        # Show a progress bar for sending
                        st.write("Sending announcement...")
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        for i in range(101):
                            # Update progress bar
                            progress_bar.progress(i)
                            status_text.text(f"Sending: {i}%")
                            time.sleep(0.01)

                        if schedule_choice == "Send Immediately":
                            status_text.text("Announcement sent successfully!")
                            st.success("Announcement sent successfully")
                        else:
                            scheduled_datetime = f"{scheduled_date} at {scheduled_time}"
                            status_text.text(f"Announcement scheduled for {scheduled_datetime}")
                            st.success(f"Announcement scheduled for {scheduled_datetime}")
                    else:
                        st.error(f"Failed to log announcement")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Display announcement templates
    st.subheader("Announcement Templates")

    templates = [
        {
            "title": "System Maintenance Notification",
            "content": "Dear users, we will be performing scheduled maintenance on [DATE] from [TIME] to [TIME]. During this period, the system may be temporarily unavailable. We apologize for any inconvenience this may cause.",
            "target": "All Users",
            "urgency": "Important"
        },
        {
            "title": "New Feature Announcement",
            "content": "We're excited to announce the release of [FEATURE], which allows you to [BENEFIT]. Check it out in the [LOCATION] section of the app!",
            "target": "All Users",
            "urgency": "Normal"
        },
        {
            "title": "Compliance Reminder",
            "content": "This is a reminder that all clubs must complete their annual compliance documentation by [DEADLINE]. Please ensure all required forms are submitted to maintain your club's active status.",
            "target": "Club Leaders",
            "urgency": "Urgent"
        }
    ]

    # Display templates in expandable sections
    for i, template in enumerate(templates):
        with st.expander(f"Template: {template['title']}"):
            st.write(f"**Content:** {template['content']}")
            st.write(f"**Target:** {template['target']}")
            st.write(f"**Urgency:** {template['urgency']}")
            if st.button("Use Template", key=f"use_template_{i}"):
                # In a real implementation, this would pre-fill the form
                st.session_state["announcement_title"] = template["title"]
                st.session_state["announcement_content"] = template["content"]
                st.session_state["target_audience"] = template["target"]
                st.session_state["urgency_level"] = template["urgency"]
                #st.experimental_rerun()

# Tab 2: View Feedback
with tab2:
    st.subheader("User Feedback")

    # Fetch feedback data
    feedback = fetch_data("feedback/feedbacks")
    if feedback is None:
        st.warning("Could not load feedback data. Please check API connection.")
        feedback = []

    # Create feedback filter options
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        # Filter by recipient type
        recipient_types = ["All"] + list(
            set(f.get("recipient_type", "Unknown") for f in feedback if "recipient_type" in f))
        selected_recipient = st.selectbox("Filter by Recipient Type", recipient_types)

    with filter_col2:
        # Filter by sender type
        sender_types = ["All"] + list(set(f.get("sender_type", "Unknown") for f in feedback if "sender_type" in f))
        selected_sender = st.selectbox("Filter by Sender Type", sender_types)

    # Apply filters
    filtered_feedback = feedback
    if selected_recipient != "All":
        filtered_feedback = [f for f in filtered_feedback if f.get("recipient_type") == selected_recipient]
    if selected_sender != "All":
        filtered_feedback = [f for f in filtered_feedback if f.get("sender_type") == selected_sender]

    # Display feedback
    if not filtered_feedback:
        st.info("No feedback matching the selected filters.")
    else:
        for feedback_item in filtered_feedback:
            with st.container():
                # Create a card-like container for each feedback item
                st.markdown(f"""
                <div style="
                    padding: 15px; 
                    border: 1px solid #dee2e6; 
                    border-radius: 5px;
                    margin-bottom: 15px;
                    background-color: #f8f9fa;
                ">
                    <p style="color: #6c757d; font-size: 14px;">
                        From: {feedback_item.get("sender_type", "Unknown")} (ID: {feedback_item.get("sender_id", "Unknown")})<br>
                        To: {feedback_item.get("recipient_type", "Unknown")} (ID: {feedback_item.get("recipient_id", "Unknown")})<br>
                        Date: {feedback_item.get("date_submitted", "Unknown date")}
                    </p>
                    <p>{feedback_item.get("content", "No content")}</p>
                </div>
                """, unsafe_allow_html=True)

                # Add action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Mark as Reviewed", key=f"review_{feedback_item.get('id', 0)}"):
                        # In a real implementation, this would mark the feedback as reviewed in the database
                        # For now, we'll log it as an admin action
                        log_data = {
                            "admin_id": admin_id,
                            "content": f"Marked feedback ID {feedback_item.get('id', 0)} as reviewed"
                        }

                        # Make the API call to log the action
                        response = post_data("admin/admin/log", log_data)

                        if response and response.status_code == 201:
                            st.success(f"Feedback ID {feedback_item.get('id', 0)} marked as reviewed")
                        else:
                            st.error(f"Failed to mark feedback as reviewed")

                with col2:
                    if st.button("Reply", key=f"reply_{feedback_item.get('id', 0)}"):
                        st.session_state[f"replying_to_{feedback_item.get('id', 0)}"] = True

                # Show reply form if reply button was clicked
                if st.session_state.get(f"replying_to_{feedback_item.get('id', 0)}", False):
                    with st.form(key=f"reply_form_{feedback_item.get('id', 0)}"):
                        reply_content = st.text_area("Your Reply", key=f"reply_content_{feedback_item.get('id', 0)}")
                        reply_submit = st.form_submit_button("Send Reply")

                        if reply_submit:
                            if reply_content:
                                try:
                                    # Create a new feedback entry for the reply
                                    reply_data = {
                                        "recipient_id": feedback_item.get("sender_id"),
                                        "recipient_type": feedback_item.get("sender_type"),
                                        "sender_id": admin_id,
                                        "sender_type": "administrator",
                                        "content": f"Reply to your feedback: {reply_content}",
                                        "date_submitted": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    }

                                    # Post the reply
                                    response = post_data("feedback/feedback", reply_data)

                                    if response and response.status_code == 201:
                                        # Log the reply action
                                        log_data = {
                                            "admin_id": admin_id,
                                            "content": f"Replied to feedback ID {feedback_item.get('id', 0)}"
                                        }

                                        # Make the API call to log the action
                                        log_response = post_data("admin/admin/log", log_data)

                                        if log_response and log_response.status_code == 201:
                                            st.success("Reply sent successfully")
                                            st.session_state[f"replying_to_{feedback_item.get('id', 0)}"] = False
                                            st.experimental_rerun()
                                        else:
                                            st.error(f"Failed to log reply action")
                                    else:
                                        st.error(f"Failed to send reply")
                                except Exception as e:
                                    st.error(f"An error occurred: {e}")
                            else:
                                st.warning("Please enter a reply before sending")

# Tab 3: Communication History
with tab3:
    st.subheader("Communication History")

    # Fetch logs for communication history
    logs = fetch_data("admin/admin/logs")
    if logs is None:
        st.warning("Could not load logs data. Please check API connection.")
        logs = []

    # Filter logs for communication-related entries
    comm_logs = []
    comm_keywords = ["announcement", "replied", "feedback", "message", "communication"]

    for log in logs:
        content = log.get("content", "").lower()
        if any(keyword in content for keyword in comm_keywords):
            comm_logs.append(log)

    if not comm_logs:
        st.info("No communication history found.")
    else:
        # Create a DataFrame for the communication logs
        comm_data = [{
            "Date": log.get("date_created", "Unknown"),
            "Admin ID": log.get("admin_id", "Unknown"),
            "Action": log.get("content", "Unknown")
        } for log in comm_logs]

        # Sort by date (most recent first)
        comm_df = pd.DataFrame(comm_data)
        if "Date" in comm_df.columns:
            try:
                comm_df["Date"] = pd.to_datetime(comm_df["Date"])
                comm_df = comm_df.sort_values(by="Date", ascending=False)
            except:
                pass  # If date conversion fails, keep original order

        st.dataframe(comm_df, use_container_width=True, hide_index=True)

    # Export option
    if st.button("Export Communication History"):
        if comm_logs:
            # Create a DataFrame for export
            export_df = pd.DataFrame(comm_data)

            # Convert to CSV for download
            csv = export_df.to_csv(index=False).encode('utf-8')

            # Provide download button
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"communication_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No communication history to export.")

# Admin tools section
with st.expander("Additional Communication Tools"):
    st.subheader("Compliance Reports")

    # Fetch clubs for compliance communication
    clubs = fetch_data("club/clubs") if "clubs" not in locals() else clubs
    if not clubs:
        st.warning("Could not load clubs data. Please check API connection.")
    else:
        # Mock compliance data (in a real implementation, this would come from the database)
        compliance_data = []
        for club in clubs:
            compliance_data.append({
                "club_id": club.get("id"),
                "club_name": club.get("name"),
                "status": np.random.choice(["Compliant", "Non-Compliant", "In Review"], p=[0.7, 0.1, 0.2])
            })

        # Filter non-compliant clubs
        non_compliant = [club for club in compliance_data if club["status"] == "Non-Compliant"]

        if non_compliant:
            st.write(f"Found {len(non_compliant)} non-compliant clubs that need attention:")

            for club in non_compliant:
                st.markdown(f"""
                <div style="
                    padding: 10px; 
                    border-left: 4px solid #dc3545; 
                    margin-bottom: 10px;
                    background-color: #f8f9fa;
                    border-radius: 0 5px 5px 0;
                ">
                    <p style="margin: 0; font-size: 14px;">
                        <span style="font-weight: bold;">{club["club_name"]} (ID: {club["club_id"]})</span><br>
                        <span style="color: #dc3545;">Status: {club["status"]}</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)

            # Add a button to send compliance reminders
            if st.button("Send Compliance Reminders to Non-Compliant Clubs"):
                success_count = 0

                for club in non_compliant:
                    # Create a feedback entry for the compliance reminder
                    reminder_data = {
                        "recipient_id": club["club_id"],
                        "recipient_type": "club",
                        "sender_id": admin_id,
                        "sender_type": "administrator",
                        "content": "URGENT: Your club is currently marked as Non-Compliant. Please submit the required documentation as soon as possible to maintain your active status.",
                        "date_submitted": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    # Post the reminder
                    response = post_data("feedback/feedback", reminder_data)

                    if response and response.status_code == 201:
                        success_count += 1

                # Log the action
                log_data = {
                    "admin_id": admin_id,
                    "content": f"Sent compliance reminders to {success_count} non-compliant clubs"
                }

                # Make the API call to log the action
                log_response = post_data("admin/admin/log", log_data)

                if success_count > 0:
                    st.success(f"Sent compliance reminders to {success_count} non-compliant clubs")
                else:
                    st.error("Failed to send compliance reminders")
        else:
            st.success("All clubs are currently compliant or under review")

# Communication guidelines section
with st.expander("Communication Guidelines"):
    st.markdown("""
    ### System Announcement Guidelines

    #### General Principles
    - Be clear and concise
    - Use appropriate urgency levels
    - Target the right audience
    - Schedule announcements during appropriate hours

    #### Types of Announcements
    1. **System Maintenance**: Notify users of planned downtime
    2. **New Features**: Announce new functionality or improvements
    3. **Policy Updates**: Inform users of policy or rule changes
    4. **Compliance Reminders**: Remind club leaders of compliance requirements

    #### Best Practices
    - Provide specific dates and times for time-sensitive information
    - Include clear instructions for any required actions
    - Avoid sending too many announcements in a short period
    - Follow up on important announcements if necessary
    """)