import streamlit as st
import re  # Import the regular expressions module
from database import execute_procedure

def add_mentor():
    st.subheader("Add Mentor")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    department = st.text_input("Department")

    # Define the regular expression for email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if st.button("Add Mentor"):
        # Check if the email matches the required format
        if not re.match(email_regex, email):
            st.error("Invalid email format! Please enter a valid email.")
        else:
            execute_procedure("AddMentor", (name, email, password, department))
            st.success(f"Mentor {name} added successfully!")

