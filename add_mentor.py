import streamlit as st
from database import execute_procedure

def add_mentor():
    st.subheader("Add Mentor")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    department = st.text_input("Department")

    if st.button("Add Mentor"):
        execute_procedure("AddMentor", (name, email, password, department))
        st.success(f"Mentor {name} added successfully!")
