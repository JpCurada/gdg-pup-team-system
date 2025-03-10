import os
import streamlit as st
import interfaces as pg

st.set_page_config(
    page_title="Data & ML",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "static\images\logo.png")

# Load custom CSS
with open(os.path.join(parent_dir, "static\styles.css")) as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# Define your pages
home = st.Page(page=pg.home_page, title='Home')
events = st.Page(page=pg.events_page, title='Events')
certificates = st.Page(page=pg.certificates_page, title='Certificates')
xparky = st.Page(page=pg.xparky_page, title='XParky')
submission = st.Page(page=pg.submission_page, title='Submission')

# Hide the default navigation but make pages available
pg = st.navigation([home, events, certificates, xparky, submission], position="hidden")

# Create a top navigation bar with right alignment
left_section,_, right_section = st.columns([2,3, 3], gap='small', vertical_alignment='center')

left_section.image("static\images\logo.png")

with right_section:
    nav_cols = st.columns(5)
    with nav_cols[0]:
        st.page_link(home, label="Home")
    with nav_cols[1]:
        st.page_link(events, label="Events")
    with nav_cols[2]:
        st.page_link(certificates, label="Certs")
    with nav_cols[3]:
        st.page_link(xparky, label="XParky")
    with nav_cols[4]:
        st.page_link(submission, label="Submission")

pg.run()