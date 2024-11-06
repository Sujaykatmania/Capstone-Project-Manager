import streamlit as st
from database import fetch_data

def display_team_info():
    st.subheader("Display Student Info")
    student_id = st.number_input("Enter Student ID", min_value=1)

    if st.button("Get Team Info"):
        result = fetch_data(f"CALL get_team_info({student_id})")
        if result:
            for row in result:
                st.write(f"Team Name: {row['Team_Name']}")
                st.write(f"Mentor: {row['Mentor_Name']}")
                st.write(f"Student Name: {row['Team_Members']}")
                # Use .get() to avoid KeyError
                st.write(f"Review: {row.get('Review', 'No review available')}")
        else:
            st.error("No data found for the provided Student ID.")
