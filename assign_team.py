import streamlit as st
from database import execute_procedure

def assign_team_to_project():
    st.subheader("Assign Team to Project")
    project_id = st.number_input("Project ID", min_value=1)
    team_id = st.number_input("Team ID", min_value=1)

    if st.button("Assign"):
        execute_procedure("AssignTeamToProject", (project_id, team_id))
        st.success(f"Assigned Team {team_id} to Project {project_id}.")
