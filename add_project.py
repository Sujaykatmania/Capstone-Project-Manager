import streamlit as st
from database import execute_procedure

def add_project():
    st.subheader("Add Project")
    project_name = st.text_input("Project Name")
    team_id = st.number_input("Team ID", min_value=1)
    mentor_id = st.number_input("Mentor ID", min_value=1)
    status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])

    if st.button("Add Project"):
        execute_procedure("AddProject", (project_name, team_id, mentor_id, status))
        st.success(f"Project {project_name} added successfully!")
