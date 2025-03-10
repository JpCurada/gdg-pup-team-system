import streamlit as st
import services.sheets_service as ss

def certificates_page():
    st.header("Download you Certificates", )
    get_certificates = ss.get_data_df("certificates")
    st.dataframe(get_certificates)
