import streamlit as st
import pandas as pd
import services.sheets_service as ss
from utils.shortcuts import show_image

def xparky_page():
    _, xparky_col, _ = st.columns([1,7, 1])
    with xparky_col:
        show_image("static\\images\\xparky-banner.svg")

        # Define the columns we need
        columns_users = ['first_name', 'last_name', 'student_number']
        columns_xp_points = ['student_number', 'xparky']

        # Search bar to search for a user's name
        search_query = st.text_input("Search your name", "")

        # Fetch the user data from the 'users' sheet
        try:
            users_data = ss.get_data_ls_dict("users")
            if isinstance(users_data, str):
                st.error(f"Error fetching users data: {users_data}")
                return
            users_df = pd.DataFrame(users_data)[columns_users]
            users_df['student_number'] = users_df['student_number'].astype(str).str.strip()
            users_df['first_name'] = users_df['first_name'].str.strip()
            users_df['last_name'] = users_df['last_name'].str.strip()
        except Exception as e:
            st.error(f"Error fetching users data: {str(e)}")
            return

        # Fetch the XParky points data from the 'xp_points' sheet
        try:
            xp_points_data = ss.get_data_ls_dict("xp_points")
            if isinstance(xp_points_data, str):
                st.error(f"Error fetching xp_points data: {xp_points_data}")
                return
            xp_points_df = pd.DataFrame(xp_points_data)[columns_xp_points]
            xp_points_df['student_number'] = xp_points_df['student_number'].astype(str).str.strip()
            
            # Replace empty strings and non-numeric values with 0 before conversion
            xp_points_df['xparky'] = pd.to_numeric(xp_points_df['xparky'], 
                                                  errors='coerce', 
                                                  downcast='integer').fillna(0)
        except Exception as e:
            st.error(f"Error fetching xp_points data: {str(e)}")
            return

        # Merge the users and XParky points data, left join to include all users
        try:
            merged_df = pd.merge(
                users_df,
                xp_points_df,
                on='student_number',
                how='left'
            )

            # Handle missing values
            merged_df['xparky'] = merged_df['xparky'].fillna(0).astype(int)
            merged_df['first_name'] = merged_df['first_name'].fillna('Unknown')
            merged_df['last_name'] = merged_df['last_name'].fillna('Student')

            # Rename columns
            merged_df = merged_df.rename(columns={
                'first_name': 'First Name',
                'last_name': 'Last Name',
                'xparky': 'XParky Points',
            })

            # Sort by XParky points in descending order
            merged_df = merged_df[['First Name', 'Last Name', 'XParky Points']].sort_values('XParky Points', ascending=False).reset_index(drop=True)

        except Exception as e:
            st.error(f"Error merging data: {str(e)}")
            return

        # Filter data based on search query
        if search_query:
            merged_df = merged_df[
                merged_df["First Name"].str.contains(search_query, case=False) | 
                merged_df["Last Name"].str.contains(search_query, case=False)
            ]

        # Display the dataframe without the index column
        if not merged_df.empty:
            display_df = merged_df.copy()
            MAX_XPARKY_POINTS = 2000
            original_points = display_df['XParky Points'].copy()
            
            st.dataframe(
                display_df,
                column_config={
                    "XParky Points": st.column_config.ProgressColumn(
                        "XParky Points",
                        help="XParky points earned out of 2000 maximum",
                        format="%d",
                        min_value=0,
                        max_value=MAX_XPARKY_POINTS,
                    ),
                },
                hide_index=True,
                use_container_width=True,
            )
            
            csv = merged_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="xparky_data.csv",
                mime="text/csv"
            )
        else:
            st.write("No data available for the search.")