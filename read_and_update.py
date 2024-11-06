import streamlit as st
from database import fetch_data, execute_procedure

def display_team_info():
    st.subheader("Display Team Info")
    student_id = st.number_input("Enter Student ID", min_value=1)
    
    if st.button("Get Team Info"):
        result = fetch_data(f"CALL get_team_info({student_id})")
        for row in result:
            st.write(f"Team Name: {row['Team_Name']}")
            st.write(f"Mentor: {row['Mentor_Name']}")
            st.write(f"Team Members: {row['Team_Members']}")
            st.write(f"Review: {row['Review']}")

def update_project_status():
    st.subheader("Update Project Status")
    project_id = st.number_input("Enter Project ID", min_value=1)
    final_submission = st.text_input("Final Submission File")
    
    if st.button("Update Project"):
        execute_procedure("after_project_update", (project_id, final_submission))
        st.success(f"Project {project_id} status updated to Completed!")
