# auth.py
from database import fetch_data, execute_query, get_teams
from add_student import add_student  # Assuming add_student handles inserting new student into the database

def sign_in(name, email, password, team_id):
    """
    Sign-in a new student by adding them to the database.
    """
    if not name or not email or not password or not team_id:
        raise ValueError("All fields must be filled out!")

    # Check if the email already exists
    existing_user_query = f"SELECT * FROM Student WHERE Email='{email}'"
    if fetch_data(existing_user_query):
        raise ValueError("Email already in use!")

    # Use add_student function to handle adding the new student
    try:
        add_student(name, email, password, team_id)  # Using team_id instead of team_name
        return True
    except Exception as e:
        raise ValueError(f"Error adding student: {e}")
