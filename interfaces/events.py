import streamlit as st
import pandas as pd
import os
import services.sheets_service as ss
from PIL import Image, ImageDraw, ImageFont
import streamlit.components.v1 as components
from utils.image_drawer import draw_text
from io import BytesIO
import base64
from streamlit_js_eval import streamlit_js_eval

# Add this at the top of your script to detect screen width
def detect_screen_width():
    # Get screen width using streamlit_js_eval
    width = streamlit_js_eval(js_expressions='window.innerWidth', want_output=True)
    
    # Store in session state
    if width is not None:
        st.session_state.screen_width = width
    elif 'screen_width' not in st.session_state:
        st.session_state.screen_width = 1200  # Default fallback

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
    .st-emotion-cache-1cvow4s a {
    color: rgb(46, 154, 255);
    text-decoration: none;
    }
    /* Mobile responsive styles */
    @media (max-width: 768px) {
        .event-container {
            flex-direction: column;
            gap: 10px;
            margin-top: 30px;
        }
        .event-text {
            padding: 15px;
            margin-top: 0;
            order: 2;
        }
        .event-image {
            padding: 10px;
            order: 1;
        }
        .event-text h2 {
            font-size: 1.8em !important;
        }
        .event-text h4 {
            font-size: 1.5em !important;
        }
        .event-text h3 {
            font-size: 1.2em !important;
        }
        .event-text p {
            font-size: 1.2em !important;
        }
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
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
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
    
    # Common CSS for styling with improved button positioning
    st.markdown("""
    <style>
    .past-events-section {
        width: 100%;
        margin-bottom: 40px;
    }
    .past-events-header {
        text-align: center;
        margin: 45px 45px 70px 45px;
        font-size: 2.5em;
        text-transform: uppercase;
        font-weight: bold;
        color: white;
    }
    .st-emotion-cache-ocqkz7 {
        display: flex;
        flex-wrap: wrap;
        -webkit-box-flex: 1;
        flex-grow: 1;
        -webkit-box-align: stretch;
        align-items: stretch;
        gap: 1rem;      
    }
    .st-emotion-cache-qcpnpn {
        background: #212121;
        min-height: 375px;
        position: relative !important;
    }
    .st-emotion-cache-qcpnpn:hover {
        transform: scale(1.05) !important;
    }
    /* Make sure the button covers everything */
    div[data-testid="stButton"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 999 !important;
    }
    div[data-testid="stButton"] > button {
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Start past events section
    st.markdown('<div class="past-events-section">', unsafe_allow_html=True)
    st.markdown('<div class="past-events-header">PAST EVENTS</div>', unsafe_allow_html=True)
    
    past_events_list = past_events.to_dict(orient="records")
    
    # Create a container for all events
    with st.container(border=False):
        # Process events in groups of 4 for each row
        for i in range(0, len(past_events_list), 4):
            # Create a row with 4 columns
            cols = st.columns(4)
            
            # Fill each column with an event
            for j, col in enumerate(cols):
                if i + j < len(past_events_list):
                    event = past_events_list[i + j]
                    
                    with col:
                        # Create a unique key for this event
                        unique_key = f"event_{i}_{j}"
                        
                        # Create a container with position relative
                        with st.container(border=True, key=unique_key):
                            # Add custom CSS for this specific container
                            st.markdown(f"""
                            <style>
                            .st-key-{unique_key} {{
                                background-color: #212121 !important;
                                color: white !important;
                                max-height: 500px !important;
                                display: flex !important;
                                flex-direction: column !important;
                                justify-content: center !important;
                                align-items: center !important;
                                text-align: center !important;
                                cursor: pointer !important;
                                position: relative !important;
                                z-index: 1 !important;
                            }}
                            .st-key-btn_{unique_key} {{
                                position: absolute !important;
                                top: 0 !important;
                                left: 0 !important;
                                width: 100% !important;
                                height: 100% !important;
                                z-index: 999 !important;
                            }}
                            .st-key-btn_{unique_key} button {{
                                width: 100% !important;
                                height: 100% !important;
                                opacity: 0 !important;
                                cursor: pointer !important;
                                position: absolute !important;
                                top: 0 !important;
                                left: 0 !important;
                            }}
                            </style>
                            """, unsafe_allow_html=True)
                            
                            # Content first (lower z-index)
                            st.markdown(f"<div class='event-title'>{event['title']}</div>", unsafe_allow_html=True)
                            st.image("static/images/gdg_card.png", use_container_width=False)
                            st.markdown(f"<div class='event-date'>{event['datetime']}</div>", unsafe_allow_html=True)
                            
                            # Button last (higher z-index)
                            # This empty space ensures the button is rendered after the content
                            st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
                            if st.button(" ", key=f"btn_{unique_key}"):
                                show_event_details(event)

    # Close section wrapper
    st.markdown('</div>', unsafe_allow_html=True)
    
def events_page():
    # First detect screen width for responsive layout
    detect_screen_width()
    
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
    
    st.markdown("""
    <style>
    .st-emotion-cache-t1wise {
        width: 100%;
        padding: 1rem 5rem 1rem 5rem;
        max-width: initial;
        min-width: auto;
    }
    .st-emotion-cache-h4xjwg {
        max-height: 0px
    }
    </style>
    """, unsafe_allow_html=True)

    show_past_events(df)