import streamlit as st
from database import execute_procedure,execute_query

def add_student():
    st.subheader("Add Student")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    team_id = st.number_input("Team ID", min_value=1)
    role = st.selectbox("Role", ["Student", "Mentor"])

    if st.button("Add Student"):
        execute_procedure("AddStudent", (name, email, password, team_id, role))
        st.success(f"Student {name} added successfully!")
