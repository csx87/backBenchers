# MySQL configurations
import mysql.connector
from flask import jsonify
import json
from datetime import datetime
import pandas as pd
import math
import decimal

# response data
# before jsonify
# dict = {"result": "int" , "msg" : <json_string>}
# msg <json_string> -> load -> list_of_elements -> each element is of dict type
#json.loads(ret['msg'])[0]["password"]

#----------- These are only fields which are configurable, avoid changing other fileds without knowledge-------------------#
config = {
    'user': 'root',
    'password': os.environ("DB Password"),
    'host': 'localhost',
    'database': 'ipl_practice_beta'
}

BACKEND_API_KEY = os.environ("BACKEND_API_KEY")
FRONTEND_API_KEY =  os.environ("FRONTEND_API_KEY")


MATCHES_WON_POINT = 2
MATCHES_LOST_POINT = 0
MATCHES_NOT_PREDICTED_POINT = -1

TEAMS_PRESENT_IN_FIRST_TOP4_PRED = 3
TEAMS_CORRECT_POSITON_PRED_FIRST_TOP4 = 3
TEAMS_PRESENT_IN_SECOND_TOP4_PRED = 2
TEAMS_CORRECT_POSITON_PRED_SECOND_TOP4 = 2

VALID_USERS = ["chaman.suresh@dish.com","srijan.sivakumar@dish.com","chethan.r@dish.com","mamidichennakeshav.m@dish.com","omkaranand.parab@dish.com","shubhammanoj.kanse@dish.com","suraj.satish@dish.com","yogish.pd@dish.com"]

FIRST_TOP4_LOCKOUT_PERIOD = "2024-03-26 00:00:00"
SECOND_TOP4_LOCKOUT_PERIOD = "2024-04-08 00:00:00"

#---------------------------------------------------------------------------------------------------------------------------#

USERS_TABLE_NAME = "users"
PREDICTION_TABLE_NAME = "predictions"
LEADERBOARD_TABLE_NAME = "leaderboard"
MATCHES_TABLE_NAME = "matches"
TEAMS_TABLE_NAME = "teams"
TOP4_TABLE_NAME = "top4"

MATCHES_ID_COL_NAME = "match_id"





PASSWORD_COL_NAME = "password"

def fetch_sql_result_and_convert_to_json(cursor, upperCase= False):
    try: 

        results_json = []
        data = cursor.fetchall()
        for row in data:
            result_dict = {}
            for i, column in enumerate(cursor.description):
            
                if isinstance(row[i], datetime):
                    # Convert datetime object to string
                    result_dict[column[0]] = row[i].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    if(isinstance(row[i], decimal.Decimal)):
                        result_dict[column[0]] = int(row[i])
                    else:
                        if(upperCase and isinstance(row[i], str)):
                            result_dict[column[0]] = row[i].upper()
                        else: 
                            result_dict[column[0]] = row[i]
            results_json.append(result_dict)
        return json.dumps(results_json)

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}
    


def execute_sql_command(command: str,fetchResults=False,parameter = None,haveToCommit = False,upperCase= False):
    result = 0
    msg = ""
    cursor = None
    try:
        # Establish a connection to the database
        with mysql.connector.connect(**config) as conn:
            if(conn != None):
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
                    
                    msg = fetch_sql_result_and_convert_to_json(cursor,upperCase)
                    
                if(haveToCommit):
                    conn.commit()
                result = 1
            else:
                msg = "Database Error: Not able to connect to database"
                result = -1
    except mysql.connector.Error as e:
        # Handle any database errors
        msg = f"Database Error: {e}"
        result = -1
    finally:
            if(cursor != None):
                cursor.close()
        
        # Check if an error occurred while fetching results
            if fetchResults and result == 1 and msg == "":
                msg = " Some error occurred while fetching results."
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
            if(len(json.loads(ret['msg'])) == 0):
                 return {"result": -1, "msg": "User_Not_Found"}

            if(password == json.loads(ret['msg'])[0]["password"]):
                return {"result": 1, "msg": ""}
            else:
                return {"result": -2, "msg": "Password doesn't match"}
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": json.loads(ret['msg'])}


def is_table_empty(table_name):
    try: 
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Execute query to count entries in the table
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return count == 0
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return -1

def excel_to_list(excel_file):
    try:
        # Read Excel file into DataFrame
        df = pd.read_excel(excel_file)

        # Convert DataFrame to list of dictionaries
        list_of_dicts = df.to_dict(orient='records')

        return list_of_dicts
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}

def excel_to_mysql(table_name,excel_file,checkTableEmpty = True):
    try:
        table_name = table_name.lower()
        df = pd.read_excel(excel_file)


        if((not checkTableEmpty) or is_table_empty(table_name)):
            insert_query = f"INSERT INTO {table_name} ("
            for column in df.columns:
                insert_query += f"{column},"
            insert_query = insert_query[:-1] + ") VALUES \n"
            for row in df.itertuples():
                insert_query = insert_query + "("
                for value in row[1:]:
                    if(type(value) is not float or not math.isnan(value) ):
                        insert_query += f"'{value}', " 
                    else:
                        insert_query += f"NULL, "
                insert_query = insert_query[:-2] + "),\n"
            insert_query = insert_query[:-2] + ";"
            ret = execute_sql_command(insert_query.lower(),haveToCommit=True)
            
            if(ret["result"] == 1):
                return execute_sql_command(f"SELECT * FROM {table_name}",fetchResults= True)
            else:
                execute_sql_command(f"DELETE FROM {table_name}",haveToCommit= True)
                ret["msg"] = "table created and constraint added but problem with data   " + ret["msg"]
                return ret
        else:
            return {"result": -1, "msg": "Table already has data please clear that"}
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}

def check_if_field_persent_in_list_of_dict(lOfDict,fields):
    for field in fields:
        for data in lOfDict:
            if(field not in data.keys()):
                return False
    return True

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
    

