import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    Hello! Welcome to HuskyPulse!! We know how much clubs and events are valued at Northeastern,
    so we thought it would be a great idea to give you all things related to that right 
    here on HuskyPulse!

    HuskyPulse offers everything you could want from an app - customer reviews, feedback on clubs, 
    personalized offerings tailored to your interests, and the best part is that it doesn't stop there. 
    HuskyPulse is the first of it's kind at Northeastern, and we hope we could develop this model to a 
    larger scale, so it can be of use to all students here at Norheastern. 

    Stay tuned for more information and features to come!
    """
        )
