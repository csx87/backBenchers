# MySQL configurations
import mysql.connector
from flask import jsonify
import json
from datetime import datetime

# response data
# before jsonify
# dict = {"result": "int" , "msg" : <json_string>}
# msg <json_string> -> load -> list_of_elements -> each element is of dict type
#json.loads(ret['msg'])[0]["password"]

config = {
    'user': 'root',
    'password': '23072000#Cs',
    'host': 'localhost',
    'database': 'wpl_final_practice'
}

BACKEND_API_KEY = '12345678'
FRONTEND_API_KEY = '12345678'

USERS_TABLE_NAME = "users"
PREDICTION_TABLE_NAME = "predictions"
LEADERBOARD_TABLE_NAME = "leaderboard"
MATCHES_TABLE_NAME = "matches"
TEAMS_TABLE_NAME = "teams"
TOP4_TABLE_NAME = "top4"

VALID_USERS = ["chaman.sureshbabu@gmail.com","yogish.pd@gmail.com","suraj.s@gmail.com","mani@gmail.com"]


PASSWORD_COL_NAME = "password"

def fetch_sql_result_and_convert_to_json(cursor):

    results_json = []
    data = cursor.fetchall()
    print("Chaman", data)
    for row in data:
        print("Chaman", row)
        result_dict = {}
        for i, column in enumerate(cursor.description):
           
            if isinstance(row[i], datetime):
                # Convert datetime object to string
                result_dict[column[0]] = row[i].strftime('%Y-%m-%d %H:%M:%S')
            else:
                print("Chaman i " , row[i])
                result_dict[column[0]] = row[i]
        results_json.append(result_dict)
    return json.dumps(results_json)


def execute_sql_command(command: str,fetchResults=False,parameter = None,haveToCommit = False):
    result = 0
    msg = ""
    try:
        print(command)
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
                #msg = str(fetch_sql_result_and_convert_to_json(cursor))
                
                msg = fetch_sql_result_and_convert_to_json(cursor)
                
            if(haveToCommit):
                conn.commit()
            result = 1
    except mysql.connector.Error as e:
        # Handle any database errors
        msg = f"Database Error: {e}"
        result = -1
    finally:
            cursor.close()
        
        # Check if an error occurred while fetching results
            if fetchResults and result == 1 and msg == "":
                msg = " Some error occurred while fetching results."
            print({"result": result, "msg": msg})
            return {"result": result, "msg": msg}

    # Indicate no results fetched


def checkPassword(user_email,password):
    try :
        query = f"SELECT " + PASSWORD_COL_NAME + " FROM " + USERS_TABLE_NAME + f" WHERE user_email=%s"
        ret = execute_sql_command(query,True,(user_email,))
        if(ret["result"]  != 1):
            return ret
        else:
            #Format of msg affects
            #print(ret['msg'],type(ret['msg']),type(json.loads(ret['msg'])[0]))
            if(password == json.loads(ret['msg'])[0]["password"]):
                return {"result": 1, "msg": ""}
            else:
                return {"result": -2, "msg": "Password doesn't match"}
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}
    

def check_if_valid_user(email):
    if(email in VALID_USERS):
        return True
    return False

def strip_after_at(email):
    at_index = email.find('@')
    if at_index != -1:
        return email[:at_index]
    else:
        return email
    

