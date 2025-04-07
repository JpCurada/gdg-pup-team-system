import streamlit as st
import pandas as pd
import services.sheets_service as ss
import time

# Use query parameters to persist login state
def check_auth_from_query_params():
    # Get query parameters
    params = st.query_params
    if "logged_in" in params and params.logged_in == "True" and "student_id" in params:
        # Re-authenticate from stored student ID
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
    """
    Authenticate the user based on their student number and password.
    """
    try:
        # Fetch the user data from the 'users' sheet
        users_data = ss.get_data_ls_dict("users")
        
        # Clean inputs
        student_number = str(student_number).strip()
        password = str(password).strip()
        
        for user in users_data:
            # Convert database values to strings and clean
            db_student_number = str(user['student_number']).strip()
            db_password = str(user['password']).strip()
            
            if db_student_number == student_number and db_password == password:
                # Store user details in session state if authentication successful
                st.session_state.user_data = user
                # Store in query params to persist across refreshes
                st.query_params.logged_in = "True"
                st.query_params.student_id = student_number
                return True
        return False
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False

def logout():
    # Clear the user data from session state and query params
    try:
        if "user_data" in st.session_state:
            del st.session_state.user_data
        if "logged_in" in st.session_state:
            st.session_state.logged_in = False
        # Clear query params
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Logout error: {str(e)}")

def submission_page():
    
    # Initialize session state for login status if it doesn't exist
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        # Check if we can restore from query params
        check_auth_from_query_params()
    
    # Initialize error tracking in session state
    if "error_message" not in st.session_state:
        st.session_state.error_message = None
    
    # Display error message if exists and then clear it
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None
    
    # Display different content based on login status
    if not st.session_state.logged_in:
        _, login_col, _ = st.columns([1,1,1])

        with login_col:
            login_container = st.container(border=False, key='login_container')
            with login_container:
                # st.image("static\images\seekliyab-banner-f.png", use_container_width=True)
                
                login_form = st.form(key="login_form", border=False)
                with login_form:
                    student_number = st.text_input("Student Number", placeholder="YYYY-DDDDD-CC-0", help="Student number that is present in your school ID")
                    password = st.text_input("Password", type="password", placeholder="SURNAME_DDDDD", help="Surname underscore then the five digits of your student number")
                    submit_button = st.form_submit_button("Submit", use_container_width=True, type="primary")
                
                if submit_button:
                    # Validate inputs
                    if not student_number or not password:
                        st.error("Please enter both student number and password")
                    else:
                        try:
                            with st.status("Authenticating...") as status:
                                if authenticate_user(student_number, password):
                                    st.session_state.logged_in = True
                                    status.update(label="Login successful!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    status.update(label="Authentication failed")
                                    st.error("Invalid student number or password")
                        except Exception as e:
                            st.session_state.error_message = f"Login error: {str(e)}"
                            st.rerun()
    else:
        try:
            # Check if user_data exists in session state
            if "user_data" not in st.session_state:
                st.session_state.error_message = "User data not found. Please log in again."
                st.session_state.logged_in = False
                st.rerun()

            # Ferry ito yung css ng activity containers, puwde mo ito i-edit
            st.markdown("""
            <style>
            /* Target all containers that have keys starting with activity_container */
            div[class*="st-key-activity_container_"] {
                height: 300px;
                background-color: var(--default-backgroundColor);
                border-radius: 10px;
                padding: 10px;
                transition: transform 0.3s;
            }

            div[class*="st-key-activity_container_"]:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }

            /* Style for the submit button */
            .stButton button {
                width: 100%;
                margin-top: auto;
            }
            </style>
            """, unsafe_allow_html=True)

            # Display user details and submission form when logged in
            st.header(f"Welcome, {st.session_state.user_data.get('first_name', 'User')}!")

            # Add logout button in the same row as the header
            col_header, col_logout = st.columns([3, 1])
            with col_logout:
                if st.button("Logout", key="logout_button"):
                    logout()

            activities_data = ss.get_data_ls_dict("activities")

            # Create 4 columns for the activities
            col1, col2, col3, col4 = st.columns(4)
            columns = [col1, col2, col3, col4]

            # Define the dialog function for submission
            @st.dialog("Activity Submission", width='large')
            def submission_dialog(activity):
                st.markdown(activity.get('instructions_markdown', 'No instructions available'))
                uploaded_file = st.file_uploader("Upload your submission", type=["pdf", "docx", "jpg", "png"])
                
                if uploaded_file is not None:
                    st.success(f"File {uploaded_file.name} uploaded successfully!")
                    # Add your file processing logic here
                    if st.button("Confirm Submission"):
                        # Handle final submission logic
                        st.success("Activity submitted successfully!")

            # Display activities in cards with borders
            for i, activity in enumerate(activities_data):
                # Determine which column to place the activity in
                col_index = i % 4
                
                # Create a container with border in the appropriate column
                with columns[col_index].container(border=True, key=f"activity_container_{i}"):
                    st.subheader(activity.get('activity_name', 'Activity'))
                    st.write(f"**Due Date:** {activity.get('due_date', 'N/A')}")
                    st.write(f"**Description:** {activity.get('description_caption', 'No description available')}")
                    # Ferry dito ilalagay kung completed naba or nah
                    st.write(f"**Status:** {activity.get('status', 'Not Completed')}")
                    
                    # Add a button for submission or details
                    if st.button("Submit", key=f"submit_{i}"):
                        # Open the dialog with the activity data
                        submission_dialog(activity)

        except Exception as e:
            st.session_state.error_message = f"Error displaying user data: {str(e)}"
            # If there's an error with the user data, reset the login state
            st.session_state.logged_in = False
            st.rerun()