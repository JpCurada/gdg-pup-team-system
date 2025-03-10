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
    
    # Common CSS that doesn't need to be repeated
    st.markdown("""
    <style>
    .st-emotion-cache-ocqkz7 {
        padding-left: 5%;
        padding-right: 5%;
        display: flex;
        flex-wrap: wrap;
        -webkit-box-flex: 1;
        flex-grow: 1;
        -webkit-box-align: stretch;
        margin-bottom: 25px;
        align-items: stretch;
        gap: 1rem;
    }     

    .past-events-section {
        width: 100%;
        margin-bottom: 40px;
    }
    .st-emotion-cache-1cvow4s a {
        text-decoration: none;
    }
    .past-events-header {
        text-align: center;
        margin: 45px 45px 70px 45px;
        font-size: 2.5em;
        text-transform: uppercase;
        font-weight: bold;
        color: white;
    }
    
    /* Desktop-specific styles */
    @media (min-width: 992px) {
        .event-card-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }
    }

    /* Tablet-specific styles */
    @media (min-width: 768px) and (max-width: 991px) {
        .event-card-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
    }

    /* Mobile-specific styles */
    @media (max-width: 767px) {
        .event-card-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        .st-emotion-cache-ocqkz7 {
            padding-left: 10px;
            padding-right: 10px;
        }
        .past-events-header {
            margin: 30px 15px 40px 15px;
            font-size: 1.8em;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Start past events section
    st.markdown('<div class="past-events-section">', unsafe_allow_html=True)

    # Header for Past Events
    st.markdown('<div class="past-events-header">PAST EVENTS</div>', unsafe_allow_html=True)

    # Define grid columns based on screen width
    # Check if we have screen width in session state
    if 'screen_width' in st.session_state and st.session_state.screen_width < 768:
        num_columns = 1  # Single column on mobile
    elif 'screen_width' in st.session_state and st.session_state.screen_width < 992:
        num_columns = 2  # Two columns on tablets
    else:
        num_columns = 4  # Default to desktop view
        
    past_events_list = past_events.to_dict(orient="records")

    # Start the event card container
    st.markdown('<div class="event-card-container">', unsafe_allow_html=True)

    # Display event cards
    for row in range(0, len(past_events_list), num_columns):
        cols = st.columns(num_columns)
        
        for i, (col, event) in enumerate(zip(cols, past_events_list[row:row + num_columns])):
            with col:
                # Load the card template for this specific event
                img = Image.open("static/images/gdg_card.png").convert("RGB")
                draw = ImageDraw.Draw(img)

                max_line_char = 922 // (32 // 2) + 5 # Estimate of max character per line
                if len(event['title']) > max_line_char:
                    y = 453  # Text needs multiple lines
                else:
                    y = 472  # Text fits in one line

                # Draw text for this specific event
                draw_text(
                    draw, 
                    text=event['title'],
                    x=88, 
                    y=y, 
                    width=922, 
                    font_size=32, 
                    font_name="medium", 
                    scale=1,
                    multiline=True
                )
                
                # Convert image to a base64-encoded data URL directly
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                card_data_url = f"data:image/png;base64,{img_str}"
                
                # Create unique key for this button
                unique_key = f"event_{row}_{i}"
                
                # Apply custom styling for this specific card
                st.markdown(f"""
                <style>
                .st-key-{unique_key} button {{
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
                
                .st-key-{unique_key} button:hover {{
                    transform: scale(1.05);
                    background-color: rgba(255, 255, 255, 0.2);
                }}
                
                .st-key-{unique_key} button p {{
                    display: none;
                }}
                
                /* Fix for mobile display */
                @media (max-width: 768px) {{
                    .st-key-{unique_key} button {{
                        min-height: 200px;
                    }}
                }}
                </style>
                """, unsafe_allow_html=True)
            
                if st.button("", key=unique_key):
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
    
    # Add Past Events section
    show_past_events(df)