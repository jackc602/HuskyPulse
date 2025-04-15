import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

SideBarLinks()

st.title("Post History")

# Retrieve posts made by this club
specifier = {"club_id": st.session_state.club_id}
response = requests.get("http://api:4000/p/posts/club", params = specifier)
response.raise_for_status()
post_data = response.json()

for post in post_data:
    st.subheader(post["title"])
    if post["is_public"]:
        pub = "Public"
    else:
        pub = "Private"
    st.write(f"{pub} Post, Created at {post['created_at']}")
    st.write(post["description"])
    if post["image_file"]:
        try:
            st.image(post["image_file"])
        except Exception as e:
            st.write(f"Image not found at path: {post['image_file']}")
    specifier = {"post_id": post["id"]}
    response = requests.get("http://api:4000/comments/post", params = specifier)
    response.raise_for_status()
    post_comments = pd.DataFrame(response.json())
    if post_comments.empty:
        st.write("No Comments Made")
    else:
        st.write("Comments:")
        st.dataframe(data = post_comments)
    
    st.divider()
    
