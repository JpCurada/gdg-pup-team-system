import os

import streamlit as st
from streamlit_navigation_bar import st_navbar

import pages as pg

st.set_page_config(
    page_title="Data & ML",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
    )

pages = ["Home", "Events", "Certificates", "XParky", "Submission"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "static\images\data-ml-logo.svg")
styles = {
    "nav": {
        "background-color": "black",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "white",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
        "font-family": "'Poppins', sans-serif",
        "font-weight": "400",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}
options = {
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    logo_path=logo_path,
    styles=styles,
    options=options,
)

functions = {
    "Home": pg.show_home,
    "Events": pg.show_events,
    "Certificates": pg.show_certificates,
    "XParky": pg.show_xparky,
    "Submission": pg.show_submission,
}
go_to = functions.get(page)
if go_to:
    go_to()