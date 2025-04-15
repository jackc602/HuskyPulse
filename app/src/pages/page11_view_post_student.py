import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Posts")

# Get current student's NUID from session
nuid = st.session_state.get("nuid")

if nuid:
    try:
        # calling the backend API so that I can extract out a certain post from a student using their NUID
        response = requests.get(f"http://api:4000/p/posts/student?nuid={nuid}")
        
        if response.status_code == 200:
            posts = response.json()
            if posts:
                st.subheader("Here are your posts:")
                for post in posts:
                    st.markdown(f"### {post['title']}")
                    st.write(post['description'])

                    if post.get("image_file"):
                        try:
                            st.image(post["image_file"], use_container_width=True)
                        except Exception as e:
                            st.warning(f"Image not found or failed to load: {post['image_file']}")

                    if post.get("created_at"):
                        try:
                            st.write(post["created_at"], use_container_width=True)
                        except Exception as e:
                            st.warning(f"Could not find the date that {post['title']}: was created at")


                    if post.get("is_public") is not None:
                        try:
                            visibility = "public" if post["is_public"] == 1 else "private"
                            st.write(f"This post can be viewed {visibility}.")
                        except Exception as e:
                            st.warning(f"Could not determine visibility for post: {e}")
                    

                    st.markdown("---")
            else:
                st.info("No posts available yet.")
        else:
            st.error("Could not fetch posts.")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("You must be logged in to see posts.")

