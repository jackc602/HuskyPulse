import streamlit as st
import requests
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
import json
import os
import uuid
from modules.nav import SideBarLinks
from modules.config import get_api_base_url

# Configure the page
st.set_page_config(
    page_title="Club Leader Dashboard - HuskyPulse",
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
        st.write(f"Debug - Accessing: {full_url} with params: {params}")
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


# Main header
st.title(f"Welcome, {st.session_state.first_name}! 🏆")
st.markdown("#### Club Leader Dashboard")

# Get club information
club_id = st.session_state.get("club_id", 1)

# Try to fetch club information
try:
    # Fetch club details
    club_info = None
    clubs = fetch_data("club/clubs")
    if clubs:
        # Find the current club in the list
        for club in clubs:
            if club.get("id") == club_id:
                club_info = club
                break

    if not club_info:
        st.error(f"Could not find club with ID {club_id}")
        club_info = {
            "id": club_id,
            "name": "Your Club",
            "type": "Unknown",
            "subject": "Unknown",
            "size": 0
        }

    # Display club information in a nice card
    with st.expander("📌 Club Information", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            # Display club logo (placeholder)
            st.image("https://place-hold.it/300x300/c8102e/ffffff&text=HC&bold", width=150)

        with col2:
            st.subheader(club_info["name"])
            st.markdown(f"**Type:** {club_info['type']}")
            st.markdown(f"**Subject:** {club_info['subject']}")
            st.markdown(f"**Size:** {club_info['size']} members")

            if st.button("✏️ Edit Club Info", key="edit_club_info"):
                st.session_state["edit_club_info"] = True
                # In a complete implementation, this would navigate to an edit page
                st.info("Club editing feature coming soon")
except Exception as e:
    st.error(f"Error loading club information: {e}")

# Create dashboard layout
col1, col2 = st.columns(2)

# Key metrics
with col1:
    st.subheader("Club Metrics")

    # Create a 2x2 grid of metric cards
    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(
            label="Active Members",
            value=club_info.get("size", 0),
            delta="5 since last month",
            delta_color="normal"
        )

        # Count pending applications
        applications = fetch_data("applications", {"club_id": club_id})
        pending_count = 0
        if applications:
            pending_count = sum(1 for app in applications if app.get("status", "").lower() == "pending")

        st.metric(
            label="Pending Applications",
            value=pending_count,
            delta=f"{pending_count} new this week",
            delta_color="normal"
        )

    with metric_col2:
        # Count posts for this club
        posts = fetch_data("p/posts/club", {"club_id": club_id})
        post_count = len(posts) if posts else 0

        st.metric(
            label="Total Posts",
            value=post_count,
            delta="N/A",
            delta_color="off"
        )

        # Count events for this club (in a real implementation)
        st.metric(
            label="Upcoming Events",
            value="N/A",
            delta="N/A",
            delta_color="off"
        )

    # Generate some example data for application trends since we don't have historical data
    chart_data = pd.DataFrame({
        'Date': pd.date_range(start=datetime.now() - timedelta(days=30), periods=31, freq='D'),
        'Applications': np.random.randint(0, 5, 31).cumsum()
    })

    # Create a line chart using Altair
    chart = alt.Chart(chart_data).mark_line(
        color='#c8102e'
    ).encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Applications:Q', title='Cumulative Applications')
    ).properties(
        title='Application Trend (Last 30 Days)'
    )

    st.altair_chart(chart, use_container_width=True)

# Quick actions
with col2:
    st.subheader("Quick Actions")

    # Create action buttons
    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("📝 Create New Post", use_container_width=True):
            st.switch_page("pages/page02_make_post.py")

        if st.button("👥 Manage Members", use_container_width=True):
            # In a real implementation, this would link to a member management page
            st.info("Feature coming soon")

    with col_b:
        if st.button("📅 Create Event", use_container_width=True):
            # In a real implementation, this would link to an event creation page
            st.switch_page("pages/page05_create_event.py")

        if st.button("📨 View Applications", use_container_width=True):
            st.switch_page("pages/page05_manage_applications.py")

    # Recent activity (simulated since we don't have actual activity data)
    st.subheader("Recent Activity")

    # Mock data for recent activity - in a real implementation, this would come from the API
    activities = [
        {"type": "application", "content": "New application received", "time": "2 hours ago"},
        {"type": "comment", "content": "New comment on your latest post", "time": "Yesterday"},
        {"type": "post", "content": "Your post reached 50 views", "time": "2 days ago"}
    ]

    for activity in activities:
        # Choose an icon based on activity type
        icon = "📋" if activity["type"] == "application" else "💬" if activity["type"] == "comment" else "📢"

        st.markdown(f"""
        <div style="
            padding: 10px; 
            border-left: 4px solid #c8102e; 
            margin-bottom: 10px;
            background-color: #f8f9fa;
            border-radius: 0 5px 5px 0;
        ">
            <p style="margin: 0; font-size: 14px;">
                <span style="font-weight: bold;">{icon} {activity["content"]}</span><br>
                <span style="color: #6c757d; font-size: 12px;">{activity["time"]}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

# Recent posts section
st.subheader("Recent Posts")

# Fetch posts for this club
posts = fetch_data("p/posts/club", {"club_id": club_id})

if posts is None:
    st.error("Could not load posts. Please try again later.")
elif len(posts) == 0:
    st.info("Your club hasn't made any posts yet.")
    if st.button("Create Your First Post", use_container_width=True):
        st.switch_page("pages/page02_make_post.py")
else:
    # Create a table for posts
    post_data = [{
        "Title": post.get("title", "Untitled"),
        "Visibility": "Public" if post.get("is_public", 0) == 1 else "Private",
        "Date": post.get("created_at", "Unknown"),
        "Actions": f"ID: {post.get('id', 'Unknown')}"
    } for post in posts]

    post_df = pd.DataFrame(post_data)
    st.dataframe(post_df, use_container_width=True, hide_index=True)

    # Button to view all posts
    if st.button("View All Posts", use_container_width=True):
        st.switch_page("pages/page03_view_post_club.py")

# Create a new post section
with st.expander("✏️ Create a New Post", expanded=False):
    st.subheader("Create a New Post")

    with st.form("new_post_form"):
        post_title = st.text_input("Post Title", max_chars=50)
        post_description = st.text_area("Post Description", max_chars=200)
        is_public = st.checkbox("Make this post public")

        post_image = st.file_uploader("Add an image (optional)")

        submit_post = st.form_submit_button("Create Post")

        if submit_post:
            if not post_title or not post_description:
                st.error("Please provide both a title and description for your post.")
            else:
                try:
                    # Handle image upload if provided
                    image_path = None
                    if post_image:
                        # In a real implementation, save the image to a proper location
                        file_ext = post_image.name.split(".")[-1]
                        image_name = f"{uuid.uuid4()}.{file_ext}"
                        image_path = f"uploads/{image_name}"

                        # Create directory if it doesn't exist
                        if not os.path.exists("uploads"):
                            os.makedirs("uploads")

                        # Save the image
                        with open(image_path, "wb") as f:
                            f.write(post_image.getbuffer())

                    # Prepare post data
                    post_data = {
                        "is_public": 1 if is_public else 0,
                        "club_id": club_id,
                        "title": post_title,
                        "description": post_description,
                        "image_file": image_path
                    }

                    # Send post data to API
                    response = requests.post(f"{API_BASE_URL}/p/posts", json=post_data)

                    if response.status_code == 200:
                        st.success("Post created successfully!")
                    else:
                        st.error(f"Error creating post: {response.text}")
                except Exception as e:
                    st.error(f"Error creating post: {e}")

# Feedback section
with st.expander("✉️ Send Announcement to Members"):
    announcement_text = st.text_area("Announcement Text", placeholder="Write your announcement here...")

    if st.button("Send Announcement", use_container_width=True):
        if announcement_text:
            # In a real implementation, this would send an announcement to all members
            st.success("Announcement sent to all members!")
        else:
            st.warning("Please write an announcement before sending.")