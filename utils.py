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

PASSWORD_COL_NAME = "password"



def execute_sql_command(command: str,fetchResults=False,parameter = None):
    result = 0
    msg = ""
    try:
        # Establish a connection to the database
        with mysql.connector.connect(**config) as conn:
            # Get cursor
            cursor = conn.cursor()

            # Execute query
            if(parameter == None):
                cursor.execute(command)
            else:
                cursor.execute(command,parameter)

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


def checkPassword(user_email,password):
    try :
        query = f"SELECT " + PASSWORD_COL_NAME + " FROM " + USERS_TABLE_NAME + f" WHERE user_email=%s"
        ret = execute_sql_command(query,True,(user_email,))
        if(ret["result"]  != 1):
            return ret
        else:
            #list->tuple
            if(password == ret['msg'][0][0]):
                return {"result": 1, "msg": ""}
            else:
                return {"result": -2, "msg": "Password doesn't match"}
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}

