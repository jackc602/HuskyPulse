# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app
import os
import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤"
    )


def WorldBankVizNav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")


## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Real_Prediction.py", label="Regression Prediction", icon="📈"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )

# Club leader role
def ClubHome():
    st.sidebar.page_link("pages/page01_club_home.py", label="Home")

def ViewPostClub():
    st.sidebar.page_link("pages/page03_view_post_club.py", label="Posts")

# Student role
def StudentHome():
    st.sidebar.page_link("pages/page10_student_home.py", label="Home")

def ViewPostStudent():
    st.sidebar.page_link("pages/page11_view_post_student.py", label="Posts")

def ApplicationStudent():
    st.sidebar.page_link("pages/page12_application_student.py", label="Applications")

# Analyst role
def AnalystHome():
    st.sidebar.page_link("pages/page30_analyst_home.py", label="Home")

def BookingData():
    st.sidebar.page_link("pages/page31_booking_data.py", label="Booking Data")

# Admin role
def AdminHome():
    st.sidebar.page_link("pages/page20_admin_home.py", label="Home")

def AdminCommunication():
    st.sidebar.page_link("pages/page21_admin_communication.py", label="Communication")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """
    base_path = os.path.dirname(__file__)
    logo_path = os.path.join(base_path, "../assets/logo.png")
    # add a logo to the sidebar always
    st.sidebar.image(logo_path, width=150)



    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Club leader sidebar
        if st.session_state["role"] == "club_leader":
            ClubHome()
            ViewPostClub()

        
        # student sidebar
        if st.session_state["role"] == "student":
            StudentHome()
            ViewPostStudent()
            ApplicationStudent()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminHome()
            AdminCommunication()

        if st.session_state["role"] == "analyst":
            AnalystHome()
            BookingData()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
