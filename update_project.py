import streamlit as st
from database import execute_query

def update_project_status():
    st.subheader("Update Project Status")
    project_id = st.number_input("Enter Project ID", min_value=1)
    final_submission = st.text_input("Final Submission File")

    if st.button("Update Project"):
        execute_query(f"UPDATE Project SET Final_Submission = '{final_submission}' WHERE Project_ID = {project_id}")
        st.success(f"Project {project_id} status updated successfully!")
