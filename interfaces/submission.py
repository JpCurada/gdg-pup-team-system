import streamlit as st
import pandas as pd
import services.sheets_service as ss
from services.drive_service import search_file, upload_file
import time


def check_auth_from_query_params():
    params = st.query_params
    if "logged_in" in params and params.logged_in == "True" and "student_id" in params:
        student_id = params.student_id
        try:
            users_data = ss.get_data_ls_dict("users")
            for user in users_data:
                if str(user['student_number']) == student_id:
                    st.session_state.user_data = user
                    st.session_state.logged_in = True
                    return True
        except Exception as e:
            st.error(f"Error restoring session: {str(e)}")
    return False

def authenticate_user(student_number, password):
    try:
        users_data = ss.get_data_ls_dict("users")
        student_number = str(student_number).strip()
        password = str(password).strip()

        for user in users_data:
            db_student_number = str(user['student_number']).strip()
            db_password = str(user['password']).strip()

            if db_student_number == student_number and db_password == password:
                st.session_state.user_data = user
                st.query_params.logged_in = "True"
                st.session_state.is_guest = True
                st.query_params.student_id = student_number
                return True
        return False
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False


def logout():
    try:
        if "user_data" in st.session_state:
            del st.session_state.user_data
        if "logged_in" in st.session_state:
            st.session_state.logged_in = False
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Logout error: {str(e)}")


def guest_sign_in():
    # Sign in as guest
    st.session_state.logged_in = True
    st.session_state.user_data = {"student_number": "Guest"}
    st.session_state.is_guest = False
    st.session_state.error_message = None


@st.dialog("Activity Details", width="large")
def show_activity_details(activity):
    st.markdown("""
    <style>
    div[data-testid="stDialog"] div[role="dialog"] {
        width: 50vw !important;  
        height: auto !important;
        margin-top: 40px;
    }

    /* Remove margin above first markdown element inside the dialog */
    div[data-testid="stDialog"] h2 {
        margin-top: -20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.write(f"## {activity['activity-name']}")
    st.markdown(activity["description-markdown"], unsafe_allow_html=True)
    st.write(f"**Instructions:** {activity['instructions']}")
    st.write(f"### Start Date: {activity['start-date']}")
    st.write(f"### Deadline: {activity['deadline']}")
    st.write(f"**XP Points:** {activity['xp_points']}")


    # Check if the user is signed in as a guest before proceeding
    if st.session_state.get("is_guest", False):
        st.markdown("""
        <div style="font-size: 24px; font-weight: bold; text-align: left;">
            Currently browsing as guest, want to submit?
        </div>
        """, unsafe_allow_html=True)

        with st.form(key="guest_signin_form", border=False):
            sign_in_button = st.form_submit_button("Sign in now")
            
            if sign_in_button:
                logout()  
    else:
        student_number = st.session_state.user_data.get("student_number", "unknown")

        folder_name = activity["activity-name"]  # Create folder based on activity name

        # Check if the user has already submitted the file
        existing_file_link = search_file(folder_name, student_number)

        if existing_file_link:
            st.success(f"✅ You have already submitted this activity! [View Submission]({existing_file_link})")
        else:
            uploaded_file = st.file_uploader("Upload a file", type=["pdf", "ipynb"])

            if uploaded_file is not None:
                with st.form(key="submit_form", border=False):
                    submit_button = st.form_submit_button("Submit File")

                    if submit_button:
                        file_link = upload_file(uploaded_file, folder_name, student_number)
                        if file_link:
                            st.success(f"File submitted successfully! [View File]({file_link})")
                            st.session_state.uploaded_file = uploaded_file
                            st.session_state.file_link = file_link
                            st.empty() 
                        else:
                            st.error("File upload failed. Please try again.")


    

def show_activities(df):
    activities = df[df['deadline'] < pd.Timestamp.now()]

    if activities.empty:
        st.markdown("<h3 style='text-align: center; color: white;'>No activities available.</h3>", unsafe_allow_html=True)
        return  

    st.markdown("""
    <style>
    .activities-section {
        width: 100%;
        margin-bottom: 40px;
    }
    .activities-header {
        text-align: center;
        margin: -20px 45px 50px 45px;
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

    st.markdown('<div class="activities-section">', unsafe_allow_html=True)
    st.markdown('<div class="activities-header">PAST ACTIVITIES</div>', unsafe_allow_html=True)
    
    activities_list = activities.to_dict(orient="records")

    with st.container(border=False):
        for i in range(0, len(activities_list), 4):
            cols = st.columns(4)
            
            for j, col in enumerate(cols):
                if i + j < len(activities_list):
                    activity = activities_list[i + j]
                    
                    with col:
                        unique_key = f"activity_{i}_{j}"
                        
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
                            
                            st.markdown(f"<div class='activity-title'>{activity['activity-name']}</div>", unsafe_allow_html=True)
                            st.image("static/images/gdg_card.png", use_container_width=False)
                            
                            if len(activity['activity-name']) <= 41:
                                st.markdown(f"<div class='activity-date'><br>{activity['start-date']}</div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div class='activity-date'>{activity['start-date']}</div>", unsafe_allow_html=True)
                            
                            st.markdown("<div style='height: 1px;'></div>", unsafe_allow_html=True)
                            if st.button(" ", key=f"btn_{unique_key}"):
                                show_activity_details(activity)

    st.markdown('</div>', unsafe_allow_html=True)


def submission_page():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        check_auth_from_query_params()

    if "error_message" not in st.session_state:
        st.session_state.error_message = None

    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None

    if not st.session_state.logged_in:
        _, login_col, _ = st.columns([1, 1, 1])
        with login_col:
            login_form = st.form(key="login_form", border=False)
            with login_form:
                student_number = st.text_input("Student Number", placeholder="YYYY-DDDDD-CC-0")
                password = st.text_input("Password", type="password", placeholder="SURNAME_DDDDD")
                submit_button = st.form_submit_button("Login")

                guest_button = st.form_submit_button("Sign in as Guest")

                if guest_button:
                    guest_sign_in()

            if submit_button:
                if not student_number or not password:
                    st.error("Please enter both student number and password.")
                else:
                    with st.status("Authenticating...") as status:
                        if authenticate_user(student_number, password):
                            st.session_state.logged_in = True
                            status.update(label="Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            status.update(label="Authentication failed")
                            st.error("Invalid student number or password")
    else:
        # If logged in, show the rest of your page
        if "user_data" not in st.session_state:
            st.session_state.error_message = "User data not found. Please log in again."
            st.session_state.logged_in = False
            st.rerun()

        # Add a fixed position logout button above the activities section
        st.markdown("""
        <style>
        .logout-button {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("Logout", key="logout_button", help="Click to logout", use_container_width=True):
            logout()

        # Show activities section below the fixed logout button
        df = ss.get_data_df("activities")
        df["start-date"] = pd.to_datetime(df["start-date"].str.extract(r'(\w+ \d{1,2}, \d{4})')[0], errors="coerce")
        df["deadline"] = pd.to_datetime(df["deadline"].str.extract(r'(\w+ \d{1,2}, \d{4})')[0], errors="coerce")
        df = df.sort_values(by="start-date", ascending=False)
        show_activities(df)

