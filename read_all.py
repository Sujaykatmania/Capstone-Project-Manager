import streamlit as st
import pandas as pd
from database import fetch_data

def read_all_data():
    st.title("All Data Overview")

    # Display Student table
    st.subheader("Students")
    query = "SELECT * FROM Student"
    students = fetch_data(query)
    if students:
        student_df = pd.DataFrame(students)  # Convert list of dicts to DataFrame
        st.dataframe(student_df)  # Display as a table
    else:
        st.write("No data found in the Students table.")

    # Display Mentor table
    st.subheader("Mentors")
    query = "SELECT * FROM Mentor"
    mentors = fetch_data(query)
    if mentors:
        mentor_df = pd.DataFrame(mentors)
        st.dataframe(mentor_df)
    else:
        st.write("No data found in the Mentors table.")

    # Display Team table
    st.subheader("Teams")
    query = "SELECT * FROM Team"
    teams = fetch_data(query)
    if teams:
        team_df = pd.DataFrame(teams)
        st.dataframe(team_df)
    else:
        st.write("No data found in the Teams table.")

    # Display Project table
    st.subheader("Projects")
    query = "SELECT * FROM Project"
    projects = fetch_data(query)
    if projects:
        project_df = pd.DataFrame(projects)
        st.dataframe(project_df)
    else:
        st.write("No data found in the Projects table.")

    # Display Evaluation table
    st.subheader("Evaluations")
    query = "SELECT * FROM Evaluation"
    evaluations = fetch_data(query)
    if evaluations:
        evaluation_df = pd.DataFrame(evaluations)
        st.dataframe(evaluation_df)
    else:
        st.write("No data found in the Evaluations table.")

    # Interconnecting data from multiple tables
    st.subheader("Interconnected Data: Teams, Students, Projects, Mentors, and Evaluations")
    query = """
    SELECT 
        T.Team_Name, 
        GROUP_CONCAT(S.Name SEPARATOR ', ') AS Team_Members,
        M.Name AS Mentor_Name,
        P.Project_Name,
        (SELECT GROUP_CONCAT(E.Grade, ' - ', E.Comments SEPARATOR '; ') 
         FROM Evaluation E WHERE E.Project_ID = P.Project_ID) AS Evaluations
    FROM Team T
    LEFT JOIN Student S ON T.Team_ID = S.Team_ID
    LEFT JOIN Mentor M ON T.Mentor_ID = M.Mentor_ID
    LEFT JOIN Project P ON T.Team_ID = P.Team_ID
    GROUP BY T.Team_ID
    """
    interconnected_data = fetch_data(query)
    if interconnected_data:
        interconnected_df = pd.DataFrame(interconnected_data)
        st.dataframe(interconnected_df)
    else:
        st.write("No interconnected data found.")
