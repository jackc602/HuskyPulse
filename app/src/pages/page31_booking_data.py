import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
from modules.nav import SideBarLinks
from modules.config import get_api_base_url
import requests

# Configure the page
st.set_page_config(layout='wide')
SideBarLinks()

# Main header
st.title("Room Booking Data Analysis")
st.write("Detailed analysis of room bookings across campus")


# Load sample data (in a real scenario, this would be fetched from the database)
@st.cache_data
def load_sample_data():
    # Create synthetic booking data
    np.random.seed(42)

    # Date range for past 6 months
    today = datetime.now()
    start_date = today - timedelta(days=180)

    # Generate dates
    dates = [start_date + timedelta(days=x) for x in range(180)]

    # Buildings and their rooms
    buildings = {
        'Snell Library': list(range(100, 110)),
        'Curry Student Center': list(range(200, 210)),
        'ISEC': list(range(300, 310)),
        'Richards Hall': list(range(400, 410)),
        'Khoury College': list(range(500, 510))
    }

    # Clubs and their types
    clubs = {
        1: "Academic",
        2: "Cultural",
        3: "Professional",
        4: "Sports",
        5: "Arts",
        6: "Social",
        7: "Service",
        8: "Religious",
        9: "Technology",
        10: "Political",
        11: "Media",
        12: "Environmental",
        13: "Health",
        14: "Gaming",
        15: "Entrepreneurship"
    }

    # Generate sample bookings
    n_bookings = 1000
    data = []

    for i in range(1, n_bookings + 1):
        building = np.random.choice(list(buildings.keys()))
        room = np.random.choice(buildings[building])
        club_id = np.random.randint(1, 16)

        # Weighted booking distribution - more bookings on weekdays
        date = np.random.choice(dates, p=np.array([
            0.18 if d.weekday() < 5 else 0.05 for d in dates
        ]) / sum([0.18 if d.weekday() < 5 else 0.05 for d in dates]))

        # Create more realistic time slots (hourly, during typical hours)
        start_hour = np.random.randint(8, 21)
        duration = np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])

        # More realistic number of attendees based on room size
        max_capacity = 10 + room % 100  # Simple formula to derive capacity from room number
        attendees = min(np.random.randint(5, max_capacity + 1), max_capacity)

        data.append({
            'booking_id': i,
            'date': date,
            'building': building,
            'room_number': room,
            'start_time': f"{start_hour:02d}:00",
            'duration_hours': duration,
            'end_time': f"{(start_hour + duration):02d}:00",
            'num_attendees': attendees,
            'club_id': club_id,
            'club_type': clubs[club_id],
            'event_type': np.random.choice(['Meeting', 'Workshop', 'Social', 'Study Group', 'Conference']),
            'capacity': max_capacity,
            'utilization': attendees / max_capacity * 100  # As a percentage
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Add derived fields
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['day_of_month'] = df['date'].dt.day

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

    # Add start_hour as integer for analysis
    df['start_hour'] = df['start_time'].apply(lambda x: int(x.split(':')[0]))
    df['end_hour'] = df['start_hour'] + df['duration_hours']
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')

    return df


# Load data
booking_data = load_sample_data()

# Sidebar for filtering data
st.sidebar.header("Filter Data")

# Date range filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=(booking_data['date'].min(), booking_data['date'].max()),
    key="sidebar_date_range"
)

# Convert date_range to datetime for filtering
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Building filter
buildings = ['All'] + sorted(booking_data['building'].unique().tolist())
selected_building = st.sidebar.selectbox("Building", buildings)

# Room type/event type filter
event_types = ['All'] + sorted(booking_data['event_type'].unique().tolist())
selected_event_type = st.sidebar.selectbox("Event Type", event_types)

# Club type filter
club_types = ['All'] + sorted(booking_data['club_type'].unique().tolist())
selected_club_type = st.sidebar.selectbox("Club Type", club_types)

# Apply filters
filtered_data = booking_data[
    (booking_data['date'] >= start_date) &
    (booking_data['date'] <= end_date)
    ]

if selected_building != 'All':
    filtered_data = filtered_data[filtered_data['building'] == selected_building]

if selected_event_type != 'All':
    filtered_data = filtered_data[filtered_data['event_type'] == selected_event_type]

if selected_club_type != 'All':
    filtered_data = filtered_data[filtered_data['club_type'] == selected_club_type]

# Display filter results
st.sidebar.markdown(f"**Showing {len(filtered_data)} bookings**")

# Main content with tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Temporal Analysis", "Space Utilization", "Raw Data"])

# Tab 1: Overview
with tab1:
    st.header("Booking Overview")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Bookings", len(filtered_data))

    with col2:
        avg_duration = round(filtered_data['duration_hours'].mean(), 1)
        st.metric("Avg. Duration (hours)", avg_duration)

    with col3:
        avg_attendees = round(filtered_data['num_attendees'].mean(), 1)
        st.metric("Avg. Attendees", avg_attendees)

    with col4:
        avg_util = round(filtered_data['utilization'].mean(), 1)
        st.metric("Avg. Utilization", f"{avg_util}%")

    # Building distribution
    st.subheader("Bookings by Building")

    building_counts = filtered_data['building'].value_counts().reset_index()
    building_counts.columns = ['Building', 'Number of Bookings']

    fig = px.bar(
        building_counts,
        x='Building',
        y='Number of Bookings',
        color='Building',
        title="Bookings by Building"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Club type and event type
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bookings by Club Type")
        club_counts = filtered_data['club_type'].value_counts().reset_index()
        club_counts.columns = ['Club Type', 'Number of Bookings']

        fig = px.pie(
            club_counts,
            values='Number of Bookings',
            names='Club Type',
            hole=0.4,
            title="Distribution by Club Type"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Bookings by Event Type")
        event_counts = filtered_data['event_type'].value_counts().reset_index()
        event_counts.columns = ['Event Type', 'Number of Bookings']

        fig = px.pie(
            event_counts,
            values='Number of Bookings',
            names='Event Type',
            hole=0.4,
            title="Distribution by Event Type"
        )
        st.plotly_chart(fig, use_container_width=True)

# Tab 2: Temporal Analysis
with tab2:
    st.header("Temporal Analysis")

    # Weekly pattern
    st.subheader("Bookings by Day of Week")

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = filtered_data['day_of_week'].value_counts().reindex(day_order).reset_index()
    day_counts.columns = ['Day of Week', 'Number of Bookings']

    fig = px.bar(
        day_counts,
        x='Day of Week',
        y='Number of Bookings',
        color='Day of Week',
        title="Bookings by Day of Week"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Monthly pattern
    st.subheader("Bookings by Month")

    # Get month order
    months_order = [calendar.month_name[i] for i in range(1, 13)]
    month_counts = filtered_data['month'].value_counts().reindex(months_order).dropna().reset_index()
    month_counts.columns = ['Month', 'Number of Bookings']

    fig = px.line(
        month_counts,
        x='Month',
        y='Number of Bookings',
        markers=True,
        title="Booking Trends by Month"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Time of day analysis
    st.subheader("Bookings by Time of Day")

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        time_period_counts = filtered_data['time_period'].value_counts().reset_index()
        time_period_counts.columns = ['Time Period', 'Number of Bookings']

        # Sort in a logical order
        time_period_order = ['Morning', 'Afternoon', 'Evening']
        time_period_counts['Time Period'] = pd.Categorical(
            time_period_counts['Time Period'],
            categories=time_period_order,
            ordered=True
        )
        time_period_counts = time_period_counts.sort_values('Time Period')

        fig = px.bar(
            time_period_counts,
            x='Time Period',
            y='Number of Bookings',
            color='Time Period',
            title="Bookings by Time Period"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Hourly distribution
        hour_counts = filtered_data['start_hour'].value_counts().sort_index().reset_index()
        hour_counts.columns = ['Hour', 'Number of Bookings']

        fig = px.bar(
            hour_counts,
            x='Hour',
            y='Number of Bookings',
            labels={'Hour': 'Starting Hour', 'Number of Bookings': 'Number of Bookings'},
            title="Bookings by Starting Hour"
        )
        fig.update_layout(xaxis=dict(tickmode='linear', tick0=8, dtick=1))
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap: Day of Week vs. Hour
    st.subheader("Booking Heatmap: Day of Week vs. Hour")

    # Prepare data for heatmap
    heatmap_data = filtered_data.groupby(['day_of_week', 'start_hour']).size().reset_index()
    heatmap_data.columns = ['Day of Week', 'Hour', 'Count']

    # Create pivot table
    pivot_data = heatmap_data.pivot(index='Day of Week', columns='Hour', values='Count').fillna(0)
    pivot_data = pivot_data.reindex(day_order)

    # Create heatmap
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Hour of Day", y="Day of Week", color="Number of Bookings"),
        x=[f"{h}:00" for h in range(8, 22)],
        y=day_order,
        color_continuous_scale="viridis",
        title="Booking Intensity by Day and Hour"
    )
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Space Utilization
with tab3:
    st.header("Space Utilization Analysis")

    # Utilization by building
    st.subheader("Average Utilization by Building")

    building_util = filtered_data.groupby('building').agg({
        'utilization': 'mean',
        'num_attendees': 'mean',
        'capacity': 'mean',
        'booking_id': 'count'
    }).reset_index()

    building_util.columns = [
        'Building',
        'Average Utilization (%)',
        'Average Attendees',
        'Average Capacity',
        'Number of Bookings'
    ]

    # Sort by utilization
    building_util = building_util.sort_values('Average Utilization (%)', ascending=False)

    # Round numerical columns
    building_util['Average Utilization (%)'] = building_util['Average Utilization (%)'].round(1)
    building_util['Average Attendees'] = building_util['Average Attendees'].round(1)
    building_util['Average Capacity'] = building_util['Average Capacity'].round(1)

    # Create chart
    fig = px.bar(
        building_util,
        x='Building',
        y='Average Utilization (%)',
        color='Building',
        hover_data=['Average Attendees', 'Average Capacity', 'Number of Bookings'],
        title="Average Space Utilization by Building"
    )

    # Add a reference line at 80% utilization
    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=len(building_util) - 0.5,
        y0=80,
        y1=80,
        line=dict(color="red", width=2, dash="dash")
    )

    # Add annotation for the reference line
    fig.add_annotation(
        x=0,
        y=80,
        xref="x",
        yref="y",
        text="Target Utilization (80%)",
        showarrow=False,
        font=dict(color="red"),
        bgcolor="white",
        bordercolor="red",
        borderwidth=1,
        xanchor="left",
        yanchor="bottom"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Room level analysis
    st.subheader("Room-Level Utilization")

    # Calculate utilization by room
    room_util = filtered_data.groupby(['building', 'room_number']).agg({
        'utilization': 'mean',
        'num_attendees': 'mean',
        'capacity': 'mean',
        'booking_id': 'count'
    }).reset_index()

    room_util.columns = [
        'Building',
        'Room Number',
        'Average Utilization (%)',
        'Average Attendees',
        'Average Capacity',
        'Number of Bookings'
    ]

    # Round numerical columns
    room_util['Average Utilization (%)'] = room_util['Average Utilization (%)'].round(1)
    room_util['Average Attendees'] = room_util['Average Attendees'].round(1)
    room_util['Average Capacity'] = room_util['Average Capacity'].round(1)

    # Create a room identifier column
    room_util['Room'] = room_util['Building'] + ' - ' + room_util['Room Number'].astype(str)

    # Sort by utilization
    room_util = room_util.sort_values('Average Utilization (%)', ascending=False)

    # Display top 10 and bottom 10 utilized rooms
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Most Utilized Rooms")
        top_rooms = room_util.head(10)

        fig = px.bar(
            top_rooms,
            x='Room',
            y='Average Utilization (%)',
            color='Building',
            hover_data=['Average Attendees', 'Average Capacity', 'Number of Bookings'],
            title="Top 10 Most Utilized Rooms"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Bottom 10 Least Utilized Rooms")
        bottom_rooms = room_util.tail(10).sort_values('Average Utilization (%)')

        fig = px.bar(
            bottom_rooms,
            x='Room',
            y='Average Utilization (%)',
            color='Building',
            hover_data=['Average Attendees', 'Average Capacity', 'Number of Bookings'],
            title="Bottom 10 Least Utilized Rooms"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Utilization by club type
    st.subheader("Utilization by Club Type")

    club_util = filtered_data.groupby('club_type').agg({
        'utilization': 'mean',
        'num_attendees': 'mean',
        'booking_id': 'count'
    }).reset_index()

    club_util.columns = [
        'Club Type',
        'Average Utilization (%)',
        'Average Attendees',
        'Number of Bookings'
    ]

    # Round numerical columns
    club_util['Average Utilization (%)'] = club_util['Average Utilization (%)'].round(1)
    club_util['Average Attendees'] = club_util['Average Attendees'].round(1)

    # Sort by utilization
    club_util = club_util.sort_values('Average Utilization (%)', ascending=False)

    fig = px.bar(
        club_util,
        x='Club Type',
        y='Average Utilization (%)',
        color='Club Type',
        hover_data=['Average Attendees', 'Number of Bookings'],
        title="Average Utilization by Club Type"
    )
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Raw Data
with tab4:
    st.header("Raw Booking Data")

    # Show the dataframe with selected columns
    display_cols = [
        'booking_id', 'date', 'building', 'room_number',
        'start_time', 'end_time', 'duration_hours',
        'club_type', 'event_type', 'num_attendees',
        'capacity', 'utilization'
    ]

    # Add download button
    csv = filtered_data[display_cols].to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="booking_data.csv",
        mime="text/csv",
    )

    # Display the dataframe
    st.dataframe(filtered_data[display_cols], use_container_width=True)

# Custom Analysis Request Form
st.markdown("---")
st.header("Request Custom Analysis from Daniel")

with st.form("detailed_analysis_request"):
    st.write("Need more detailed analysis? Submit a request to Daniel (System Analyst):")

    analysis_title = st.text_input("Analysis Title", "Room Booking Optimization Analysis")

    analysis_type = st.multiselect(
        "Analysis Types (Select multiple if needed)",
        [
            "Historical Trends",
            "Building Comparison",
            "Capacity Planning",
            "Club/Event Type Analysis",
            "Optimization Recommendations",
            "Forecasting",
            "Custom Charts/Visualizations",
            "Other"
        ],
        default=["Historical Trends"]
    )

    specific_buildings = st.multiselect(
        "Specific Buildings to Focus On (Optional)",
        options=booking_data['building'].unique()
    )

    specific_question = st.text_area(
        "Specific Questions or Analysis Goals",
        "I'd like to understand which rooms are consistently underutilized and could be repurposed or made available for additional events."
    )

    required_by = st.date_input(
        "Analysis Required By",
        value=datetime.now() + timedelta(days=7)
    )

    contact_preference = st.radio(
        "Preferred Contact Method",
        ["Email", "Meeting", "Phone Call"]
    )

    submitted = st.form_submit_button("Submit Request to Daniel")

    if submitted:
        # Here you would typically save this to a database or send via API
        st.success(
            "Your detailed analysis request has been sent to Daniel! He will contact you within 1-2 business days.")

        # Display submission details
        st.write("**Request Details:**")
        st.write(f"- Analysis Title: {analysis_title}")
        st.write(f"- Analysis Types: {', '.join(analysis_type)}")
        if specific_buildings:
            st.write(f"- Focus Buildings: {', '.join(specific_buildings)}")
        st.write(f"- Required By: {required_by}")
        st.write(f"- Contact Preference: {contact_preference}")