import streamlit as st
from database import execute_procedure

def assign_team_to_project():
    st.subheader("Assign Team to Project")
    project_id = st.number_input("Project ID", min_value=1)
    team_id = st.number_input("Team ID", min_value=1)
    
    if st.button("Assign"):
        execute_procedure("AssignTeamToProject", (project_id, team_id))
        st.success(f"Assigned Team {team_id} to Project {project_id}.")

def evaluate_project():
    st.subheader("Evaluate Project")
    project_id = st.number_input("Project ID", min_value=1)
    panel_id = st.number_input("Panel ID", min_value=1)
    grade = st.number_input("Grade", min_value=0.0, max_value=10.0)
    comments = st.text_area("Comments")
    
    if st.button("Evaluate"):
        execute_procedure("EvaluateProject", (project_id, panel_id, grade, comments))
        st.success(f"Project {project_id} evaluated with grade {grade}.")
