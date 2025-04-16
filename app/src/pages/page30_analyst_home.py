import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from modules.nav import SideBarLinks
from modules.config import get_api_base_url
import requests

# Configure the page
st.set_page_config(layout='wide')
SideBarLinks()

# Main header
st.title(f"Welcome {st.session_state.first_name}!")
st.subheader("Analytics Dashboard")

# Create tabs for different analysis sections
tab1, tab2, tab3 = st.tabs(["Booking Overview", "Usage Patterns", "Recommendations"])


# Load sample data (in a real scenario, this would be fetched from the database)
@st.cache_data
def load_sample_data():
    # Create synthetic booking data
    np.random.seed(42)

    # Date range for past 3 months
    today = datetime.now()
    start_date = today - timedelta(days=90)

    # Generate dates
    dates = [start_date + timedelta(days=x) for x in range(90)]

    # Buildings
    buildings = ['Snell Library', 'Curry Student Center', 'ISEC', 'Richards Hall', 'Khoury College']

    # Generate sample bookings
    n_bookings = 500
    data = {
        'booking_id': range(1, n_bookings + 1),
        'date': np.random.choice(dates, n_bookings),
        'building': np.random.choice(buildings, n_bookings),
        'room_number': np.random.randint(100, 500, n_bookings),
        'start_time': [f"{np.random.randint(8, 21):02d}:00" for _ in range(n_bookings)],
        'duration_hours': np.random.choice([1, 2, 3], n_bookings),
        'num_attendees': np.random.randint(1, 30, n_bookings),
        'club_id': np.random.randint(1, 20, n_bookings),
        'event_type': np.random.choice(['Meeting', 'Workshop', 'Social', 'Study Group', 'Other'], n_bookings)
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Add day of week
    df['day_of_week'] = df['date'].dt.day_name()

    # Add time period
    def categorize_time(time_str):
        hour = int(time_str.split(':')[0])
        if hour < 12:
            return 'Morning'
        elif hour < 17:
            return 'Afternoon'
        else:
            return 'Evening'

    df['time_period'] = df['start_time'].apply(categorize_time)

    # Calculate end time and format as string
    df['end_time'] = df.apply(lambda row: f"{(int(row['start_time'].split(':')[0]) + row['duration_hours']):02d}:00",
                              axis=1)

    return df


# Load the data
booking_data = load_sample_data()

# Convert booking_data to a more usable format for time analysis
booking_data['date_str'] = booking_data['date'].dt.strftime('%Y-%m-%d')
booking_data['start_hour'] = booking_data['start_time'].apply(lambda x: int(x.split(':')[0]))
booking_data['end_hour'] = booking_data['start_hour'] + booking_data['duration_hours']

# Tab 1: Booking Overview
with tab1:
    st.header("Booking Overview")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Bookings", len(booking_data))
    with col2:
        st.metric("Unique Rooms", len(booking_data[['building', 'room_number']].drop_duplicates()))
    with col3:
        avg_duration = round(booking_data['duration_hours'].mean(), 1)
        st.metric("Avg. Duration (hours)", avg_duration)
    with col4:
        avg_attendees = round(booking_data['num_attendees'].mean(), 1)
        st.metric("Avg. Attendees", avg_attendees)

    # Booking distribution by building
    st.subheader("Bookings by Building")
    building_counts = booking_data['building'].value_counts().reset_index()
    building_counts.columns = ['Building', 'Count']
    fig = px.bar(building_counts, x='Building', y='Count', color='Building')
    st.plotly_chart(fig, use_container_width=True)

    # Booking trends over time
    st.subheader("Booking Trends (Past 3 Months)")
    bookings_per_day = booking_data.groupby('date_str').size().reset_index()
    bookings_per_day.columns = ['Date', 'Bookings']
    fig = px.line(bookings_per_day, x='Date', y='Bookings')
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Usage Patterns
with tab2:
    st.header("Usage Patterns")

    col1, col2 = st.columns(2)

    # Day of week analysis
    with col1:
        st.subheader("Bookings by Day of Week")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = booking_data['day_of_week'].value_counts().reindex(day_order).reset_index()
        day_counts.columns = ['Day', 'Count']
        fig = px.bar(day_counts, x='Day', y='Count', color='Day')
        st.plotly_chart(fig, use_container_width=True)

    # Time of day analysis
    with col2:
        st.subheader("Bookings by Time of Day")
        time_counts = booking_data['time_period'].value_counts().reset_index()
        time_counts.columns = ['Time Period', 'Count']
        fig = px.pie(time_counts, values='Count', names='Time Period', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap of bookings by hour and day
    st.subheader("Booking Heatmap (Hour vs Day)")

    # Prepare data for heatmap
    hour_day_counts = booking_data.groupby(['day_of_week', 'start_hour']).size().reset_index()
    hour_day_counts.columns = ['Day', 'Hour', 'Count']

    # Create pivot table
    pivot_data = hour_day_counts.pivot(index='Day', columns='Hour', values='Count').fillna(0)
    pivot_data = pivot_data.reindex(day_order)
    

    # Create heatmap
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Hour of Day", y="Day of Week", color="Number of Bookings"),
        x=pivot_data.columns,  # 14 labels: 8 to 21
        y=day_order,
        color_continuous_scale="viridis"
    )

    st.plotly_chart(fig, use_container_width=True)
    

    # Event type distribution
    st.subheader("Bookings by Event Type")
    event_counts = booking_data['event_type'].value_counts().reset_index()
    event_counts.columns = ['Event Type', 'Count']
    fig = px.bar(event_counts, x='Event Type', y='Count', color='Event Type')
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Recommendations
with tab3:
    st.header("Data-Driven Recommendations")

    # Calculate utilization by building
    building_util = booking_data.groupby('building').agg({
        'booking_id': 'count',
        'num_attendees': 'mean',
        'duration_hours': 'mean'
    }).reset_index()

    building_util.columns = ['Building', 'Number of Bookings', 'Average Attendees', 'Average Duration (hours)']

    # Show the data
    st.dataframe(building_util)

    # Generate insights
    st.subheader("Key Insights")

    # Most popular building
    most_popular = building_util.loc[building_util['Number of Bookings'].idxmax()]['Building']
    st.write(f"🔍 **Most popular building**: {most_popular}")

    # Busiest day
    busiest_day = day_counts.loc[day_counts['Count'].idxmax()]['Day']
    st.write(f"🔍 **Busiest day of week**: {busiest_day}")

    # Busiest time period
    busiest_time = time_counts.loc[time_counts['Count'].idxmax()]['Time Period']
    st.write(f"🔍 **Busiest time period**: {busiest_time}")

    # Most common event type
    most_common_event = event_counts.loc[event_counts['Count'].idxmax()]['Event Type']
    st.write(f"🔍 **Most common event type**: {most_common_event}")

    # Underutilized spaces
    least_used = building_util.loc[building_util['Number of Bookings'].idxmin()]['Building']
    st.write(f"🔍 **Least utilized building**: {least_used}")

    # Recommendations section
    st.subheader("Recommendations")

    st.markdown("""
    Based on the booking data analysis, here are some recommendations:

    1. **Capacity Planning**: Consider adding more rooms or expanding capacity at {most_popular} since it's the most frequently booked building.

    2. **Scheduling**: Since {busiest_day} is the busiest day, consider extending hours or adding more rooms available on this day.

    3. **Resource Allocation**: The {busiest_time} time period has the highest demand; ensure adequate staffing and resources during this time.

    4. **Promotion Strategy**: {least_used} is underutilized; consider promoting this space more, especially for {most_common_event} events which are the most common.

    5. **Event Support**: Since the average event duration is {avg_duration} hours with {avg_attendees} attendees, optimize support services accordingly.
    """.format(
        most_popular=most_popular,
        busiest_day=busiest_day,
        busiest_time=busiest_time,
        least_used=least_used,
        most_common_event=most_common_event,
        avg_duration=avg_duration,
        avg_attendees=round(avg_attendees)
    ))

    # Export options
    st.subheader("Export Options")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate PDF Report", use_container_width=True):
            st.success("PDF report would be generated here in a real implementation")

    with col2:
        if st.button("Share Insights via Email", use_container_width=True):
            st.success("Email sharing functionality would be implemented here")

# Bottom section - connection with Daniel
st.markdown("---")
st.header("Connect with Daniel for Custom Analysis")

# Form for requesting custom analysis
with st.form("custom_analysis_form"):
    st.write("Need a custom analysis? Submit your request to Daniel (System Analyst):")

    analysis_type = st.selectbox(
        "Analysis Type",
        ["Space Utilization", "Attendance Trends", "Building Comparison", "Event Type Analysis", "Other"]
    )

    date_range = st.date_input(
        "Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        key="date_range"
    )

    specific_buildings = st.multiselect(
        "Specific Buildings (Optional)",
        options=booking_data['building'].unique()
    )

    additional_notes = st.text_area("Additional Notes or Requirements")

    submitted = st.form_submit_button("Submit Request to Daniel")

    if submitted:
        # Here we would typically save this request to a database or send it via an API
        st.success("Your analysis request has been sent to Daniel! He will contact you shortly.")

        # Display a confirmation with details
        st.write("**Request Details:**")
        st.write(f"- Analysis Type: {analysis_type}")
        st.write(f"- Date Range: {date_range[0]} to {date_range[1]}")
        if specific_buildings:
            st.write(f"- Buildings: {', '.join(specific_buildings)}")
        if additional_notes:
            st.write(f"- Additional Notes: {additional_notes}")