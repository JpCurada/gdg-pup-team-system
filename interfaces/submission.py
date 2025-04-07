import streamlit as st
import pandas as pd
import services.sheets_service as ss

<<<<<<< HEAD
def submission_page():
    st.header("Submission")

=======
@st.dialog("Event Details", width="large")
def show_event_details(event):
    st.markdown("""
    <style>
    div[data-testid="stDialog"] div[role="dialog"] {
        width: 50vw !important;  
        height: auto !important;
        margin-top: 40px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.video(event["link"])
    st.write(f"## {event['title']}")
    st.write(event['datetime'])
    st.write(event['type'])
    st.write(event['description'])

def show_past_events(df):
    past_events = df[df['status'] == 'Done']
    
    if past_events.empty:
        st.markdown("<h3 style='text-align: center; color: white;'>No past events available.</h3>", unsafe_allow_html=True)
        return  

    st.markdown("""
    <style>
    .past-events-section {
        width: 100%;
        margin-bottom: 40px;
    }
    .past-events-header {
        text-align: center;
        margin: -20px 45px 50px 45px; /* Reduced top margin */
        font-size: 2.5em;
        text-transform: uppercase;
        font-weight: bold;
        color: white;
    }

    .st-emotion-cache-ocqkz7 {
        display: flex;
        flex-wrap: wrap;
        flex-grow: 1;
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

    st.markdown('<div class="past-events-section">', unsafe_allow_html=True)
    st.markdown('<div class="past-events-header">SUBMISSIONS</div>', unsafe_allow_html=True)
    
    past_events_list = past_events.to_dict(orient="records")

    with st.container(border=False):
        for i in range(0, len(past_events_list), 4):
            cols = st.columns(4)
            
            for j, col in enumerate(cols):
                if i + j < len(past_events_list):
                    event = past_events_list[i + j]
                    
                    with col:
                        unique_key = f"event_{i}_{j}"
                        
                        with st.container(border=True, key=unique_key):
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
                            
                            st.markdown(f"<div class='event-title'>{event['title']}</div>", unsafe_allow_html=True)
                            st.image("static/images/gdg_card.png", use_container_width=False)
                            
                            if len(event['title']) <= 41:
                                st.markdown(f"<div class='event-date'><br>{event['datetime']}</div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div class='event-date'>{event['datetime']}</div>", unsafe_allow_html=True)
                            
                            st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
                            if st.button(" ", key=f"btn_{unique_key}"):
                                show_event_details(event)

    st.markdown('</div>', unsafe_allow_html=True)

def submission_page():
    df = ss.get_data_df("events")
    df["event_date"] = pd.to_datetime(df["datetime"].str.extract(r'(\w+ \d{1,2}, \d{4})')[0], errors="coerce")
    df = df.sort_values(by="event_date", ascending=False)
    
    show_past_events(df)
>>>>>>> 623bc1f7d6906b23a4417189b5a8082b551053ed
