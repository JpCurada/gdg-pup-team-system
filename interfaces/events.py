import streamlit as st
import pandas as pd
import os
import services.sheets_service as ss
from PIL import Image, ImageDraw, ImageFont
import streamlit.components.v1 as components
from utils.title import draw_text, image_url

def display_event(event):
    st.markdown("""
    <style>
    .event-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        min-height: 300px;
        max-height: 700px;
        margin-top: 60px;
        padding-bottom: 30px;
    }
    .event-text {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        padding: 20px 20px 20px 90px;
        margin-top: -47px; 
    }
    .event-image {
        flex: 1;
        display: flex;
        align-items: center;
        padding-right: 30px;
        justify-content: center;
    }
    .event-image img {
        max-width: 100%;
        max-height: 700px;
        object-fit: contain;
    }
    .event-button-container {
        display: flex;
        align-items: center;
        margin-top: 20px;
    }
    .event-button {
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 5px;
        font-size: 1em;
        margin-right: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Determine event header and button dynamically
    if event["status"] == "Upcoming":
        event_header = "UPCOMING EVENT"
        button_text = "RSVP NOW"
        button_color = "blue"
    else:  # When event is "Done"
        event_header = "LATEST EVENT"
        button_text = "VIEW DETAILS"
        button_color = "#505050"

    # Ensure image path is valid
    event_image = event.get("link", "").strip()

    # Ensure the link is valid
    event_link = event.get("link", "#").strip()

    # Button HTML (always show "View Details" for Done events)
    event_button_html = f'''
    <div class="event-button-container">
        <a href="{event_link}" class="event-button" style="background-color: {button_color}; color: white;">
            {button_text}
        </a>
    </div>
    '''

    # Event container
    st.markdown(f"""
    <div class="event-container">
        <div class="event-text">
            <h2 style="font-size: 2.5em;">{event_header} - {event['datetime']}</h2>
            <h4 style="font-size: 2.0em; margin: 20px 0px 0px 0px;">{event['title']}</h4>
            <h3 style="font-size: 1.5em;">{event['type']}</h3>
            <p style="font-size: 1.6em; margin: 0;">{event['description']}</p>
            {event_button_html}  <!-- Button will always be present now -->
        </div>
        <div class="event-image">
            <img src="{event_image}" alt="Event Image">
        </div>
    </div>
    """, unsafe_allow_html=True)

@st.dialog("Event Details")
def show_event_details(event):
    st.write(f"## {event['title']}")
    st.write(f"**Date:** {event['datetime']}")
    st.write(f"**Type:** {event['type']}")
    st.write(f"**Description:** {event['description']}")
    # Add any other event details you want to display

def show_past_events(df):
    # Filter only past events
    past_events = df[df['status'] == 'Done']
    
    if past_events.empty:
        st.markdown("<h3 style='text-align: center; color: white;'>No past events available.</h3>", unsafe_allow_html=True)
        return  # Exit early if no past events
    
    # Load the card template
    img = Image.open("static/images/gdg_card.png").convert("RGB")

    # Create a draw object
    draw = ImageDraw.Draw(img)

    # Generate cards for past events
    for index, row in past_events.iterrows():  
        draw_text(
            draw, 
            text=row['title'],
            x=0, 
            y=460, 
            width=1098, 
            font_size=48, 
            font_name="regular", 
            multiline=True
        )

    # Convert modified image to URL
    card_data_url = image_url(img)

    # Define styles dynamically
    st.markdown(f"""
    <style>
    .st-emotion-cache-ocqkz7 {{
        padding-left: 90px;
        padding-right: 75px;
        display: flex;
        flex-wrap: wrap;
        -webkit-box-flex: 1;
        flex-grow: 1;
        -webkit-box-align: stretch;
        margin-bottom: 25px;
        align-items: stretch;
        gap: 1rem;
    }}     

    .past-events-section {{
        width: 100%;
        margin-bottom: 40px;
    }}
    .st-emotion-cache-1cvow4s a {{
    text-decoration: none;
    }}
    .past-events-header {{
        text-align: center;
        margin: 45px 45px 70px 45px;
        font-size: 2.5em;
        text-transform: uppercase;
        font-weight: bold;
        color: white;
    }}

    .stButton > button {{
        width: 100%;
        height: 100%;
        background-color: transparent;
        border: 2px solid #333;
        border-radius: 10px;
        overflow: hidden;
        cursor: pointer;
        transition: transform 0.3s ease;
        padding: 0;
        display: block;
        position: relative;
        min-height: 255px;
        background-image: url('{card_data_url}');
        background-size: cover;
        background-position: center;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.05);
        background-color: rgba(255, 255, 255, 0.2);
    }}
    
    .stButton > button p {{
        display: none;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Start past events section
    st.markdown('<div class="past-events-section">', unsafe_allow_html=True)

    # Header for Past Events
    st.markdown('<div class="past-events-header">PAST EVENTS</div>', unsafe_allow_html=True)

    # Define grid columns
    num_columns = 4
    past_events_list = past_events.to_dict(orient="records")

    # Display event cards
    for row in range(0, len(past_events_list), num_columns):
        cols = st.columns(num_columns)
        
        for i, (col, event) in enumerate(zip(cols, past_events_list[row:row + num_columns])):
            with col:
                unique_key = f"event_{row}_{i}"
                if st.button("", key=unique_key):
                    show_event_details(event)
    
    # Close section wrapper
    st.markdown('</div>', unsafe_allow_html=True)

    
def events_page():
    df = ss.get_data_df("events")
    
    # Extract only the date part from the 'datetime' column
    df["event_date"] = pd.to_datetime(df["datetime"].str.extract(r'(\w+ \d{1,2}, \d{4})')[0], errors="coerce")
    
    # Sort by event_date in descending order to get the latest event first
    df = df.sort_values(by="event_date", ascending=False)
    
    # Show the latest 'Upcoming' event first
    upcoming_event = df[df["status"] == "Upcoming"].head(1)
    if not upcoming_event.empty:
        display_event(upcoming_event.iloc[0])
    else:
        # If no 'Upcoming' events exist, show the latest event regardless of status
        latest_event = df.head(1)
        display_event(latest_event.iloc[0])
    
    # Add Past Events section
    show_past_events(df)


