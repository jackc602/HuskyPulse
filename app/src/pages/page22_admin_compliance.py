import streamlit as st
import requests
import pandas as pd
from modules.config import get_api_base_url


API_BASE_URL = get_api_base_url()

st.set_page_config(layout="wide")
st.title("Compliance Management")

# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.warning("Please log in first.")
    st.stop() # Stop execution if not authenticated

# Attempt to get Admin ID from session state
admin_id = st.session_state.get("user_id", None)
if admin_id is None:
    # Assuming 'role' is also stored in session state to confirm it's an admin
    if st.session_state.get("role") == "admin":
         st.error("Admin ID not found in session state. Please log in again.")
    else:
         st.error("Access denied. Admin privileges required.")
    st.stop()

# --- Helper Function for API Calls ---
def make_api_request(method, endpoint, json_data=None, params=None):
    """Generic function to make API requests, handling errors."""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.request(method, url, json=json_data, params=params)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        # Check content type before assuming JSON
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            return response.json()
        else:
            # Log or handle non-JSON responses appropriately if expected
            # st.warning(f"Received non-JSON response from {endpoint}: {response.text[:100]}...")
            return None # Or return response.text if that's useful
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Failed ({method} {endpoint}): {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred during API request: {e}")
        return None

# --- Function to Fetch Compliance Data ---
@st.cache_data(ttl=30) # Cache for 30 seconds to allow near real-time updates
def get_compliance_data(status_filter=None):
    """Fetches compliance records from the API, optionally filtered by status."""
    endpoint = "/compliance"
    params = {}
    if status_filter and status_filter != "All":
        params['status'] = status_filter # API needs to support this query parameter

    response_data = make_api_request("GET", endpoint, params=params)

    if response_data and isinstance(response_data, list):
        if not response_data:
            return pd.DataFrame() # Return empty DataFrame if list is empty
        try:
            # Convert list of dicts to DataFrame
            df = pd.DataFrame(response_data)
            # Define expected columns based on zoe_routes.py and schema
            expected_cols = ['id', 'status', 'admin_id', 'club_id']
            # Ensure essential columns exist, fill missing ones with None/NaN
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = pd.NA # Use pandas NA for missing values
            return df[expected_cols] # Select and order columns
        except Exception as e:
            st.error(f"Error processing compliance data into DataFrame: {e}")
            return pd.DataFrame()
    # Handle cases where API might return a message dict instead of list (if API does this)
    elif response_data and isinstance(response_data, dict) and 'message' in response_data:
         st.warning(f"API Message: {response_data['message']}")
         return pd.DataFrame()
    else:
        return pd.DataFrame()

# --- UI Elements ---
st.header("View Compliance Requests")

# Status Filter (using statuses from inserts.sql)
status_options = ["All", "Pending Review", "Requires Clarification", "Awaiting Approval", "Approved", "Non-Compliant", "Overdue", "Exempt", "Expired", "Partially Compliant", "Completed"]
selected_status = st.selectbox("Filter by Status:", options=status_options, index=0)

# Fetch and display data
compliance_df = get_compliance_data(selected_status)

if not compliance_df.empty:
    st.dataframe(
        compliance_df,
        use_container_width=True,
        hide_index=True,
        column_config={ # Optional: configure column display
            "id": st.column_config.NumberColumn("Record ID"),
            "status": st.column_config.TextColumn("Status"),
            "admin_id": st.column_config.NumberColumn("Admin ID"),
            "club_id": st.column_config.NumberColumn("Club ID")
        }
    )

    st.divider()
    st.header("Update Compliance Status")

    # Filter for records that typically require action
    actionable_statuses = ['Pending Review', 'Requires Clarification', 'Awaiting Approval']
    actionable_records = compliance_df[compliance_df['status'].isin(actionable_statuses)]

    if not actionable_records.empty:
        record_id_to_update = st.selectbox(
            "Select Compliance Record ID to Update:",
            options=actionable_records['id'].tolist(),
            help="Select a record currently needing action.",
            key="compliance_id_select"
        )

        if record_id_to_update:
            # Possible actions/statuses Admin can set
            new_status_options = ["Approved", "Non-Compliant", "Requires Clarification"]
            new_status = st.selectbox(
                "Select New Status:",
                options=new_status_options,
                key="new_status_select" # Add key for stability
            )
            update_button = st.button(f"Update Record {record_id_to_update} to '{new_status}'")

            if update_button:
                # Prepare payload as expected by the PUT /compliance/{id} endpoint in zoe_routes.py
                update_payload = {
                    "status": new_status,
                    "admin_id": admin_id # Use the logged-in admin's ID
                }
                endpoint = f"/compliance/{record_id_to_update}"
                response = make_api_request("PUT", endpoint, json_data=update_payload)

                if response is not None:
                    if isinstance(response, dict):
                         if 'message' in response:
                              st.success(response['message'])
                         elif 'id' in response:
                              st.success(f"Successfully updated compliance record {response['id']} to status '{response.get('status', new_status)}'.")
                         else:
                              st.success(f"Compliance record {record_id_to_update} updated. API response: {response}")
                    else:
                         st.success(f"Compliance record {record_id_to_update} update request sent. Response: {response}")

                    # Clear cache and rerun to show updated data
                    st.cache_data.clear()
                    # Use st.rerun() in newer Streamlit versions
                    try:
                        st.rerun()
                    except AttributeError:
                        st.experimental_rerun()
                else:
                    st.error(f"Failed to update compliance record {record_id_to_update}. Check API logs if necessary.")
        else:
            st.info("Select a compliance record ID from the list above to update its status.")
    else:
        st.info(f"No compliance records found with statuses requiring action ({', '.join(actionable_statuses)}).")

elif selected_status:
     st.info(f"No compliance records found with status '{selected_status}'.")
else:
     st.info("No compliance records available to display.")

# Manual refresh button
if st.button("Refresh Data"):
    st.cache_data.clear()
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()