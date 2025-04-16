import logging
import streamlit as st
import os
import uuid
import requests
from datetime import datetime
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
SideBarLinks()

current_file = os.path.abspath(__file__)
src_dir = os.path.dirname(os.path.dirname(current_file))

st.title("Create New Post")

name = st.text_input("Title:")

public_status = int(st.checkbox("Public Post?"))

desc = st.text_area("Description:")

img = st.file_uploader("Cover Image")

if st.button("Upload Post"):
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
                 "image_file": save_path
             }
         else:
             post_data = {
                 "is_public": public_status,
                 "club_id": st.session_state.club_id,
                 "title": name,
                 "description": desc,
                 "image_file": None
             }
         try:
             response = requests.post("http://api:4000/p/posts", json = post_data)
             if response.status_code == 200:
                 st.success("Post created Successfully!")
                 logger.info(f"Post added with data {post_data}")
         except Exception as e:
             st.error(f"Error Making Post. {e}")

if st.button("Back"):
    st.switch_page("pages/page01_club_home.py")
