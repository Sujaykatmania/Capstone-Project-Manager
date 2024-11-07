import streamlit as st
import re
from database import execute_procedure, execute_query

def add_student():
    st.subheader("Add Student")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    team_id = st.number_input("Team ID", min_value=1)
    role = st.selectbox("Role", ["Student", "Mentor"])

    # Email validation regex
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{2,}$'

    if st.button("Add Student"):
        # Check if the email matches the required format
        if not re.match(email_regex, email):
            st.error("Invalid email format! Please enter a valid email address.")
        else:
            execute_procedure("AddStudent", (name, email, password, team_id, role))
            st.success(f"Student {name} added successfully!")
