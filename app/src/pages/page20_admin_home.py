import streamlit as st
import requests
from modules.nav import SideBarLinks
from modules.config import get_api_base_url

SideBarLinks()

st.title("Welcome, Olivia (System Admin)")
st.subheader("System Management Dashboard")

admin_id = 1  # hardcoded for demo
API_BASE_URL = get_api_base_url()


# ---- Assign Role ----
st.write("### Assign Role")
with st.form("assign_role_form"):
    role_name = st.text_input("Role Name", "Club_Manager")
    if st.form_submit_button("Assign Role"):
        try:
            response = requests.post(f"{API_BASE_URL}/admin/assign-role", json={
                "admin_id": admin_id,
                "role_name": role_name
            })
            st.write("Status Code:", response.status_code)
            st.write("Raw Response Text:", response.text)

            if response.status_code == 201:
                try:
                    st.success(response.json().get("message", "Role assigned."))
                except requests.exceptions.JSONDecodeError:
                    st.error("Server response is not valid JSON.")
            else:
                st.error(f"Request failed: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")


# ---- Log Compliance Status ----
st.write("### Log Compliance Status")
with st.form("compliance_form"):
    club_id = st.number_input("Club ID", step=1)
    status = st.selectbox("Status", ["FERPA Compliant", "Non-Compliant", "In Review"])
    if st.form_submit_button("Log Compliance"):
        try:
            response = requests.post(f"{API_BASE_URL}/admin/compliance", json={
                "admin_id": admin_id,
                "club_id": club_id,
                "status": status
            })
            st.write("Status Code:", response.status_code)
            st.write("Raw Response Text:", response.text)

            if response.status_code == 201:
                try:
                    st.success(response.json().get("message", "Compliance logged."))
                except requests.exceptions.JSONDecodeError:
                    st.error("Server response is not valid JSON.")
            else:
                st.error(f"Request failed: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")


# ---- Log Action or Integration ----
st.write("### Log Action or Integration")
with st.form("log_form"):
    content = st.text_area("Log Content", "Performed a system audit...")
    if st.form_submit_button("Log Action"):
        try:
            response = requests.post(f"{API_BASE_URL}/admin/log", json={
                "admin_id": admin_id,
                "content": content
            })
            st.write("Status Code:", response.status_code)
            st.write("Raw Response Text:", response.text)

            if response.status_code == 201:
                try:
                    st.success(response.json().get("message", "Action logged."))
                except requests.exceptions.JSONDecodeError:
                    st.error("Server response is not valid JSON.")
            else:
                st.error(f"Request failed: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")


# ---- Log Backup Event ----
st.write("### Log Backup Event")
with st.form("backup_form"):
    content = st.text_area("Backup Info", "Full backup scheduled at midnight.")
    if st.form_submit_button("Log Backup"):
        try:
            response = requests.post(f"{API_BASE_URL}/admin/backup", json={
                "admin_id": admin_id,
                "content": content
            })
            st.write("Status Code:", response.status_code)
            st.write("Raw Response Text:", response.text)

            if response.status_code == 201:
                try:
                    st.success(response.json().get("message", "Backup logged."))
                except requests.exceptions.JSONDecodeError:
                    st.error("Server response is not valid JSON.")
            else:
                st.error(f"Request failed: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
