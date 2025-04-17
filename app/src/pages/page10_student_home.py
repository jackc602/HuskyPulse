import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
from modules.nav import SideBarLinks
from modules.config import get_api_base_url


# Configure the page
st.set_page_config(
    page_title="Student Dashboard - HuskyPulse",
    page_icon="🐺",
    layout="wide"
)

API_BASE_URL = get_api_base_url()

# response = requests.get(f"{API_BASE_URL}/c/clubs")



# Initialize navigation
SideBarLinks()

# Get API base URL
API_BASE_URL = get_api_base_url()


# Function to fetch data from API with given endpoint and optional params
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
st.title(f"Welcome, {st.session_state.first_name}! 👋")
st.markdown("#### Your HuskyPulse Dashboard")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["📣 Feed", "🔍 Discover Clubs", "📋 My Applications"])


with tab1:
    student_id = st.session_state.get("nuid", 1)

    st.subheader("Latest Club Posts")

    posts = fetch_data("p/posts/student", {"nuid": student_id})

    if not posts:
        st.info("No posts found. This could be due to an API connection issue or no available posts.")
        posts = [] 

    if len(posts) == 0:
        st.info("No posts to display. Join some clubs to see their posts here!")
    else:
        for post in posts:
            # Create a card for each post
            with st.container():
                st.markdown(f"""
                <div style="
                    padding: 15px; 
                    border: 1px solid #dee2e6; 
                    border-radius: 5px;
                    margin-bottom: 15px;
                ">
                    <h4 style="margin-top: 0;">{post.get("title", "Untitled Post")}</h4>
                    <p style="color: #6c757d; font-size: 14px;">Club ID: {post.get("club_id", "Unknown")} • {post.get("created_at", "Unknown date")}</p>
                    <p>{post.get("description", "No description available")}</p>
                    <p>Visibility: {"Public" if post.get("is_public", 0) == 1 else "Private"}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("💬 Comment", key=f"comment_{post.get('id', 0)}"):
                    st.session_state[f"commenting_{post.get('id', 0)}"] = True

                if st.session_state.get(f"commenting_{post.get('id', 0)}", False):
                    comment = st.text_area("Your comment:", key=f"comment_text_{post.get('id', 0)}")
                    if st.button("Submit Comment", key=f"submit_comment_{post.get('id', 0)}"):
                        if comment:
                            try:
                                data = {
                                    "nuid": st.session_state.nuid,
                                    "comment": str(comment),
                                    "post_id": int(post["id"])
                                }
                                response = requests.post("http://api:4000/comments/post", json = data)
                                st.write(response.status_code)
                            except Exception as e:
                                st.error(f"Error submitting comment: {e}")
                            st.success("Comment Posted")
                        else:
                            st.warning("Please enter a comment.")

                st.markdown("---")

# Tab 2: Discover Clubs - Browse and search for clubs
with tab2:
    st.subheader("Discover Clubs")

    # Search and filter options
    col1, col2 = st.columns(2)

    with col1:
        search_term = st.text_input("Search clubs:", placeholder="Enter club name or keyword")

    with col2:
        filter_options = st.multiselect(
            "Filter by type:",
            ["Academic", "Cultural", "Professional", "Sports", "Arts", "Community Service", "Technology", "Other"]
        )

    # Fetch all clubs
    clubs = fetch_data("club/clubs")

    if not clubs:
        st.error("Could not load clubs data. Please try again later.")
    else:
        # Filter clubs based on search term and filters
        filtered_clubs = clubs
        if search_term:
            filtered_clubs = [club for club in filtered_clubs if
                              search_term.lower() in club.get("name", "").lower() or
                              search_term.lower() in club.get("type", "").lower() or
                              search_term.lower() in club.get("subject", "").lower()]

        if filter_options:
            filtered_clubs = [club for club in filtered_clubs if club.get("type", "") in filter_options]

        # Display clubs
        if len(filtered_clubs) == 0:
            st.info("No clubs match your search criteria.")
        else:
            # Create a row of club cards (3 per row)
            for i in range(0, len(filtered_clubs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(filtered_clubs):
                        club = filtered_clubs[i + j]
                        with cols[j]:
                            st.markdown(f"""
                            <div style="
                                padding: 15px; 
                                border: 1px solid #dee2e6; 
                                border-radius: 5px;
                                height: 200px;
                                overflow: hidden;
                            ">
                                <h4 style="margin-top: 0;">{club.get("name", "Unnamed Club")}</h4>
                                <p>Type: {club.get("type", "N/A")}<br>
                                Subject: {club.get("subject", "N/A")}<br>
                                Members: {club.get("size", "Unknown")}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button("Apply", key=f"apply_club_{club.get('id', 0)}"):
                                st.session_state["apply_club_id"] = club.get('id', 0)
                                st.switch_page("pages/page13_apply_student.py")

# Tab 3: My Applications - View and track application status
with tab3:
    st.subheader("My Applications")

    # Fetch the student's applications
    applications = fetch_data("applications", {"applicant_id": student_id})

    if not applications:
        st.info("No applications found or API connection issue.")
        applications = []  # Set to empty list if None

    if len(applications) == 0:
        st.info("You haven't applied to any clubs yet.")
        if st.button("Browse Clubs to Apply"):
            st.switch_page("pages/page11_browse_clubs.py")
    else:
        # Create a table of applications
        app_data = [{
            "Application ID": app.get("id", "Unknown"),
            "Club ID": app.get("club_id", "Unknown"),
            "Status": app.get("status", "Pending").capitalize(),
            "Club Name": app.get("club_name", "Unnamed Club"),
        } for app in applications]

        app_df = pd.DataFrame(app_data)
        st.dataframe(app_df, use_container_width=True, hide_index=True)

# Recommendations section
st.markdown("---")
st.subheader("🎯 Recommended Clubs Based on Your Interests")

# Fetch personalized recommendations
recommendations = fetch_data("recommend/recommendations", {"applicant_id": student_id})

if not recommendations:
    st.info("No recommendations available at this time.")
else:
    # Display recommendations in a horizontal scrollable area
    if len(recommendations) == 0:
        st.info("No recommendations available yet. Apply to more clubs to get personalized suggestions!")
    else:
        # Create rows of recommendations (3 per row)
        for i in range(0, len(recommendations), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(recommendations):
                    club = recommendations[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div style="
                            padding: 15px; 
                            border: 1px solid #dee2e6; 
                            border-radius: 5px;
                            height: 150px;
                            overflow: hidden;
                            background-color: #f8f9fa;
                        ">
                            <h4 style="margin-top: 0;">{club.get("name", "Unnamed Club")}</h4>
                            <p>Type: {club.get("type", "N/A")}<br>
                            Subject: {club.get("subject", "N/A")}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("View Details", key=f"rec_view_{club.get('id', 0)}"):
                            st.session_state["view_club_id"] = club.get('id', 0)
                            # In a complete implementation, you would navigate to a club details page

# Feedback section
st.markdown("---")
with st.expander("📝 Submit Feedback for HuskyPulse"):
    with st.form("feedback_form"):
        content = st.text_area("What would you like to share about HuskyPulse?",
                               placeholder="We'd love to hear your thoughts so we can make this app better for everyone!")
        submitted = st.form_submit_button("Submit Feedback")

        if submitted and content.strip():
            try:
                # Prepare feedback data
                feedback_data = {
                    "recipient_id": 0,  # System feedback
                    "recipient_type": "system",
                    "sender_id": student_id,
                    "sender_type": "student",
                    "content": content,
                    "date_submitted": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                # Post feedback to API
                response = requests.post(f"{API_BASE_URL}/feedback/feedback", json=feedback_data)
                if response.status_code == 201:
                    st.success("Thank you for your feedback!")
                else:
                    st.error(f"Error submitting feedback: {response.text}")
            except Exception as e:
                st.error(f"Error submitting feedback: {e}")
        elif submitted:
            st.warning("Please write your feedback before submitting.")