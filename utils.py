# MySQL configurations
import mysql.connector

config = {
    'user': 'root',
    'password': '23072000#Cs',
    'host': 'localhost',
    'database': 'wpl_practice'
}

BACKEND_API_KEY = '12345678'
FRONTEND_API_KEY = '12345678'

USERS_TABLE_NAME = "users"
PREDICTION_TABLE_NAME = "predictions"
LEADERBOARD_TABLE_NAME = "leaderboard"
MATCHES_TABLE_NAME = "matches"
TEAMS_TABLE_NAME = "teams"



def execute_sql_command(command: str, fetchResults=False):
    result = 0
    msg = ""
    try:
        # Establish a connection to the database
        with mysql.connector.connect(**config) as conn:
            # Get cursor
            cursor = conn.cursor()

            # Execute query
            cursor.execute(command)

            # Fetch results if requested
            if fetchResults:
                msg = cursor.fetchall()
            result = 1
    except mysql.connector.Error as e:
        # Handle any database errors
        msg = f"Database Error: {e}"
        result = -1
    finally:
        # Ensure cursor is closed
        if 'cursor' in locals():
            cursor.close()
        
        # Check if an error occurred while fetching results
        if fetchResults and not msg:
            msg = "Some error occurred while fetching results."
            result = 0
        
        return {"result": result, "msg": msg}

    # Indicate no results fetched

