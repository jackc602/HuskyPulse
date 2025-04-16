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


# Quick actions
with col2:
    st.subheader("Quick Actions")

    # Create action buttons

    if st.button("📝 Create New Post", use_container_width=True):
        st.switch_page("pages/page02_make_post.py")


    if st.button("📅 Create Event", use_container_width=True):
        # In a real implementation, this would link to an event creation page
        st.switch_page("pages/page05_create_event.py")

    if st.button("📨 View Applications", use_container_width=True):
        st.switch_page("pages/page07_view_applications.py")

   
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
    } for post in posts]

    post_df = pd.DataFrame(post_data).head(5)
    st.dataframe(post_df, use_container_width=True, hide_index=True)

    # Button to view all posts
    if st.button("View All Posts", use_container_width=True):
        st.switch_page("pages/page03_view_post_club.py")

