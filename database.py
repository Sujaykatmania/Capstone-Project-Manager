import mysql.connector
from mysql.connector import Error
import streamlit as st

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="dbms_project"
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_procedure(proc_name, args):
    """
    Executes a stored procedure with the given name and arguments.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc(proc_name, args)
            conn.commit()
        except Error as e:
            print(f"Error executing procedure {proc_name}: {e}")
        finally:
            cursor.close()
            conn.close()

def execute_query(query, params=None):
    """
    Executes a query with optional parameters.
    Parameters:
    - query: The SQL query string
    - params: A tuple of parameters to execute with the query (default is None)
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())  # If no params, use an empty tuple
            conn.commit()
        except Error as e:
            print(f"Error executing query: {e}")
            st.error(f"An error occurred while executing the query: {e}")
        finally:
            cursor.close()
            conn.close()

def fetch_data(query, params=None):
    """
    Fetches data from the database for a given query with optional parameters.
    Parameters:
    - query: The SQL query string
    - params: A tuple of parameters for the query (default is None)
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())  # If no params, use an empty tuple
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

def get_teams():
    """
    Fetches available teams from the database.
    """
    query = "SELECT Team_ID, Team_Name FROM Team;"
    return fetch_data(query)  # Assuming fetch_data fetches results from a query
