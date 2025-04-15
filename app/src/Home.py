##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title("Welcome to HuskyPulse!")
st.write('\n\n')
st.write('### Hi! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Zoe, leader of the Hawaii Club", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'club_leader'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'Zoe'
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    st.session_state["club_id"] = 1
    logger.info("Logging in as Club Leader Persona")
    st.switch_page('pages/page01_club_home.py')

if st.button('Act as Charlie, a Northeastern Student',
            type = 'primary',
            use_container_width=True):
	st.session_state['authenticated'] = True
	st.session_state['role'] = 'student'
	st.session_state['first_name'] = 'Charlie'
	st.session_state["nuid"] = 1
	st.switch_page('pages/page10_student_home.py')

if st.button('Act as Olivia, System Administrator',
             type='primary', use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'Olivia'
    st.switch_page('pages/page20_admin_home.py')

if st.button('Act as Daniel, the System Analyst',
            type = 'primary', 
            use_container_width=True):
	st.session_state['authenticated'] = True
	st.session_state['role'] = 'analyst'
	st.session_state['first_name'] = 'Daniel'
	st.switch_page('pages/page20_admin_home.py')

