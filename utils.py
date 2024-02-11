# MySQL configurations
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



def executeSqlCommand(conn,command: str, fetchResults=False):
    try:
        print(command)
        # Get cursor
        cursor = conn.cursor()

        # Execute query
        cursor.execute(command)

        # Fetch results if requested
        if fetchResults:
            return cursor.fetchall()
    except mysql.connector.Error as e:
        # Handle any database errors
        print(f"Error executing SQL command: {e}")
        return str(e)

    return None  # Indicate no results fetched

