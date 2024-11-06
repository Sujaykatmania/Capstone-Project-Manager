import streamlit as st
from database import get_connection

def delete_student():
    st.title("Delete Student")
    
    student_id = st.number_input("Student ID", min_value=1, step=1)
    
    if st.button("Delete Student"):
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Student WHERE Student_ID = %s"
        cursor.execute(query, (student_id,))
        conn.commit()
        st.success("Student deleted successfully.")
        cursor.close()
        conn.close()
