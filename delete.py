import streamlit as st
from database import get_connection

def delete_student():
    st.title("Delete Student")
    
    student_id = st.number_input("Student ID", min_value=1, step=1)
    
    if st.button("Delete Student"):
        conn = get_connection()
        cursor = conn.cursor()

        # Check if the student exists
        check_query = "SELECT COUNT(*) FROM Student WHERE Student_ID = %s"
        cursor.execute(check_query, (student_id,))
        result = cursor.fetchone()

        if result[0] > 0:
            # If student exists, delete the record
            delete_query = "DELETE FROM Student WHERE Student_ID = %s"
            cursor.execute(delete_query, (student_id,))
            conn.commit()
            st.success("Student deleted successfully.")
        else:
            st.error("Student does not exist.")
        
        cursor.close()
        conn.close()
