import streamlit as st
import services.sheets_service as ss
import utils.certificates as ct

def certificates_page():
    _, middle, _ = st.columns(spec=[1,2,1])

    with middle:   
        st.header("Download your certificates here")
        
        email_input = st.text_input("Enter the email that you entered on the evaluation forms below: ")
        
        if st.button("Enter", type="secondary") or st.session_state.get('form_submitted', False):
            # Set a flag to indicate the form was submitted
            st.session_state.form_submitted = True
            
            event_participated_table = ss.get_data_ls_dict("event_participated")
            event_id_participated = [event['event_id'] for event in event_participated_table if event['email'] == email_input]

            if event_id_participated:    
                certificates_table = ss.get_data_ls_dict("certificates")
                event_title_participated = [event["title"] for event in certificates_table if event["event_id"] in event_id_participated]
                cert_to_print = st.selectbox("Which event would you like a certificate for?", event_title_participated)

                selected_cert_info = [info for info in certificates_table if info["title"] == cert_to_print]
                selected_cert_info = selected_cert_info[0]

                user_table = ss.get_data_ls_dict("users")
                user_row = next((row for row in user_table if row["email"] == email_input), None)

                # Add a "Generate Certificate" button to control when to generate/show the certificate
                if st.button("Generate Certificate"):

                    cert = ct.cert_maker(
                        user_row["first_name"] + " " + user_row["last_name"],
                        selected_cert_info["type"], 
                        selected_cert_info["title"], 
                        selected_cert_info["tech_team"], 
                        selected_cert_info["certificate_description"], 
                        selected_cert_info["date"], 
                        selected_cert_info["gdg_lead_name"], 
                        selected_cert_info["tech_team_lead"], 
                        selected_cert_info["tech_team_colead"]
                    )

                   
                    st.image(cert)

                    cert.save("temp.jpg")

                    # Add a download button
                    with open("temp.jpg", "rb") as file:
                        st.download_button(
                            label="Download Certificate",
                            data=file,
                            file_name=user_row["last_name"] + "_" + selected_cert_info["title"] + ".jpg",
                            mime="image/jpg",
                            on_click="ignore"
                        )
            else:
                st.warning('You have not yet participated in any of our events', icon="ℹ️")
