import streamlit as st
import pandas as pd

def show_xparky():
    st.header("XParky Tracker")

    # Sample DataFrame
    data = {
        "First Name": ["John", "Jane", "Doe"],
        "Last Name": ["Smith", "Doe", "Johnson"],
        "XParky Points": [1500, 2300, 1800],
        "Student Number": [101, 102, 103],
    }
    df = pd.DataFrame(data)

    # Search functionality (simplified for markdown)
    st.text_input(
        "Search your name",
        placeholder="Enter first or last name..."
    )

    # Display table
    st.table(
        df.drop(columns=['Student Number'])
    )

    # Download button
    st.download_button(
        label="Download XParky Data",
        data=df.to_csv(index=False),
        file_name="xparky_points.csv",
        mime="text/csv"
    )
