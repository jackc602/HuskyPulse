import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import os
import uuid
from modules.nav import SideBarLinks

SideBarLinks()

specifier = {"post_id": st.session_state.post_to_edit}
post_response = requests.get("http://api:4000/p/posts", params = specifier)
post_data = post_response.json()[0]


st.title("Edit Post")

name = st.text_input("Title:", value = post_data["title"])

public_status = int(st.checkbox("Public Post?", value = bool(post_data["is_public"])))

desc = st.text_area("Description:", value = post_data["description"])

event = st.text_input("Event", value = post_data["event_id"]) # TODO: need another route to get events by the club, make dropdown

img = st.file_uploader("Cover Image")

if st.button("Save Changes"):
    if not name or not desc:
        st.error("Post must have a title and description.")
    else:
        # if user uploads an image save it to assets folder and store 
        # the path to insert into the database
        if img is not None:
            file_ext = img.name.split(".")[-1]
            img_name = f"{uuid.uuid4()}.{file_ext}"
            save_path = os.path.join(os.getcwd(), "assets", img_name)

            with open(save_path, "wb") as outfile:
                outfile.write(img.getbuffer())
            post_data = {
                "is_public": public_status,
                "club_id": st.session_state.club_id,
                "title": name,
                "description": desc,
                "image_file": save_path,
                "event_id": event,
                "post_id": st.session_state.post_to_edit
            }
        else:
            post_data = {
                "is_public": public_status,
                "club_id": st.session_state.club_id,
                "title": name,
                "description": desc,
                "image_file": None,
                "event_id": event,
                "post_id": st.session_state.post_to_edit
            }
        try:
            response = requests.post("http://api:4000/p/update", json = post_data)
            st.success("Post created Successfully!")
            logger.info(f"Post {post_data['post_id']} was updated")
        except Exception as e:
            st.error(f"Error Making Post. {e}")

if st.button("Back"):
    st.switch_page("pages/page03_view_post_club.py")