import streamlit as st
from database import fetch_data, execute_query
from add_student import add_student
from evaluate_project import evaluate_project
from read_all import read_all_data
from display_team import display_team_info
from add_mentor import add_mentor
from assign_team import assign_team_to_project  # Import the assign team function
from delete import delete_student  # Import the delete student function
from update_project import update_project_status  # Import the update project function

# Function to initialize session state
def initialize_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'is_signing_in' not in st.session_state:
        st.session_state.is_signing_in = False
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

# Function for login
def login(email, password):
    query = f"SELECT * FROM Student WHERE Email='{email}' AND Password='{password}'"
    user_data = fetch_data(query)

    if user_data:
        st.session_state.user = user_data[0]  # Assuming the first result is the user
        st.session_state.logged_in = True
        st.session_state.user['Role'] = 'Student'  # Explicitly set the role for a student
    else:
        st.error("Invalid email or password!")

# Function for mentor login
def mentor_login(email, password):
    query = f"SELECT * FROM Mentor WHERE Email='{email}' AND Password='{password}'"
    user_data = fetch_data(query)

    if user_data:
        st.session_state.user = user_data[0]  # Assuming the first result is the user
        st.session_state.logged_in = True
        st.session_state.user['Role'] = 'Mentor'  # Explicitly set the role for a mentor
    else:
        st.error("Invalid email or password!")

# Function for admin login
def admin_login(email, password):
    admin_email = "admin@123"  # Change to your admin email
    admin_password = "lol"  # Change to your admin password

    if email == admin_email and password == admin_password:
        st.session_state.is_admin = True
        st.session_state.logged_in = True
        # Create a dummy admin user object
        st.session_state.user = {
            'Name': 'Admin',  # Set a name for the admin
            'Role': 'Admin'   # Set the role as Admin
        }
        st.success("Logged in as Admin")  # Add success message
    else:
        st.error("Invalid admin credentials!")

# Function to handle sign-in
def sign_in(name, email, password, team_name):
    query = f"INSERT INTO Student (Name, Email, Password, Team_ID) VALUES ('{name}', '{email}', '{password}', '{team_name}')"
    try:
        execute_query(query)  # Assuming this function executes a given SQL command
        st.success("Sign-in successful! You can now log in.")
        st.session_state.is_signing_in = False  # Reset sign-in state after success
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to display student options
def student_options():
    student_id = st.session_state.user['Student_ID']
    student_info = fetch_data(f"CALL get_student_info({student_id});")
    st.write("Your Information:")
    st.table(student_info)

# Function to display mentor options
def mentor_options():
    mentor_id = st.session_state.user['Mentor_ID']
    teams = fetch_data(f"SELECT * FROM Team WHERE Mentor_ID={mentor_id};")
    st.write("Teams under you:")
    for team in teams:
        st.write(f"Team Name: {team['Team_Name']}")
        st.write("Students in this team:")
        students = fetch_data(f"SELECT * FROM Student WHERE Team_ID={team['Team_ID']};")
        st.table(students)
        st.write("\n")

# Function to display admin options
def admin_options():
    st.header("Admin Dashboard")

    # Display the options as a sidebar menu
    menu = ["Add Student", "Add Mentor", "Evaluate Project", "View All Records", 
            "Display Student Info", "Assign Team to Project", "Delete Student", 
            "Update Project Status"]
    choice = st.sidebar.selectbox("Admin Menu", menu)

    if choice == "Add Student":
        add_student()

    elif choice == "Add Mentor":
        add_mentor()

    elif choice == "Evaluate Project":
        evaluate_project()

    elif choice == "View All Records":
        read_all_data()  # View all records option

    elif choice == "Display Student Info":
        display_team_info() 

    elif choice == "Assign Team to Project":
        assign_team_to_project()

    elif choice == "Delete Student":
        delete_student()

    elif choice == "Update Project Status":
        update_project_status()

# Main app function
def main():
    st.title("Capstone Project Manager")

    initialize_session_state()

    if not st.session_state.logged_in:
        st.header("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # Login buttons for different roles
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Login as Student"):
                login(email, password)

        with col2:
            if st.button("Login as Mentor"):
                mentor_login(email, password)

        # Admin login section
        st.subheader("Admin Login")
        admin_email = st.text_input("Admin Email")
        admin_password = st.text_input("Admin Password", type="password")
        if st.button("Login as Admin"):
            admin_login(admin_email, admin_password)

        # Sign-in section for new students
        if st.button("Sign In (New Student)"):
            st.session_state.is_signing_in = True

        if st.session_state.is_signing_in:
            st.subheader("Sign In")
            name = st.text_input("Name")
            new_email = st.text_input("Email (for Sign In)")
            new_password = st.text_input("Password (for Sign In)", type="password")

            # 1. Fetch team names and IDs
            teams = fetch_data("SELECT Team_ID, Team_Name FROM Team")
            team_options = {team["Team_Name"]: team["Team_ID"] for team in teams}

            # 2. Dropdown to select team by name, storing the ID
            selected_team_name = st.selectbox("Select Team", list(team_options.keys()))  # Display names
            team_id = team_options[selected_team_name]  # Get the corresponding team_id

            # 3. Use team_id in the sign_in function
            if st.button("Submit Sign In"):
                sign_in(name, new_email, new_password, team_id)  # Use team_id
    else:
        # Welcome message and options for logged-in users
        st.header("Welcome!")
        if st.session_state.user is not None and "Name" in st.session_state.user:
            st.write(f"Logged in as: {st.session_state.user['Name']}")
        else:
            st.error("User not found. Please log in again.")
        
        # Logout button
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.logged_in = False
            st.session_state.is_admin = False

        # Check user role safely
        if st.session_state.user is not None and "Role" in st.session_state.user:
            if st.session_state.user["Role"] == "Student":
                student_options()  # You will need to define this function elsewhere
            elif st.session_state.user["Role"] == "Mentor":
                mentor_options()  # You will need to define this function elsewhere
            elif st.session_state.is_admin:
                admin_options()
        else:
            st.error("User role not found. Please log in again.")

if __name__ == "__main__":
    main()  