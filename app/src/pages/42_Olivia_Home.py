import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Welcome, Olivia (System Admin)")
st.subheader("System Management Dashboard")

admin_id = 1  # hardcoded for demo
API_BASE_URL = "http://web-api:4000"

st.write("### Assign Role")
with st.form("assign_role_form"):
    role_name = st.text_input("Role Name", "Club_Manager")
    if st.form_submit_button("Assign Role"):
        r = requests.post("http://localhost:4000/admin/assign-role", json={
            "admin_id": admin_id,
            "role_name": role_name
        })
        st.success(r.json().get("message"))

st.write("### Log Compliance Status")
with st.form("compliance_form"):
    club_id = st.number_input("Club ID", step=1)
    status = st.selectbox("Status", ["FERPA Compliant", "Non-Compliant", "In Review"])
    if st.form_submit_button("Log Compliance"):
        r = requests.post("http://localhost:4000/admin/compliance", json={
            "admin_id": admin_id,
            "club_id": club_id,
            "status": status
        })
        st.success(r.json().get("message"))

st.write("### Log Action or Integration")
with st.form("log_form"):
    content = st.text_area("Log Content", "Performed a system audit...")
    if st.form_submit_button("Log Action"):
        r = requests.post("http://localhost:4000/admin/log", json={
            "admin_id": admin_id,
            "content": content
        })
        st.success(r.json().get("message"))

st.write("### Log Backup Event")
with st.form("backup_form"):
    content = st.text_area("Backup Info", "Full backup scheduled at midnight.")
    if st.form_submit_button("Log Backup"):
        r = requests.post("http://localhost:4000/admin/backup", json={
            "admin_id": admin_id,
            "content": content
        })
        st.success(r.json().get("message"))

