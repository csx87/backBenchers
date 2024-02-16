# MySQL configurations
import mysql.connector
from flask import jsonify
import json
from datetime import datetime
import pandas as pd
import math

# response data
# before jsonify
# dict = {"result": "int" , "msg" : <json_string>}
# msg <json_string> -> load -> list_of_elements -> each element is of dict type
#json.loads(ret['msg'])[0]["password"]

config = {
    'user': 'root',
    'password': 'GILLisGOAT@77',
    'host': 'localhost',
    'database': 'wpl_practice_beta'
}

BACKEND_API_KEY = '123456789'
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


def setup_tables():
    try:
        with open("tables_setup.txt", 'r') as file:
            queries = file.read().split(';')[:-1]
            for query in queries:
                ret = execute_sql_command(query,haveToCommit=True)
                if(ret != 1):
                    return ret 
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}
    


def excel_to_mysql(table_name,excel_file,constraint_file):
    try:
        table_name = table_name.lower()
        df = pd.read_excel(excel_file)

        create_table_query = f"CREATE TABLE {table_name} ("
        for column in df.columns:
            create_table_query += f"{column}, \n"
        create_table_query = create_table_query[:-3] + ");"
        print(create_table_query + "\n")

        if(constraint_file != None):
            alter_table_query = f"ALTER TABLE {table_name}\n"
            with open(constraint_file, "r") as file:
                for line in file:
                    alter_table_query = alter_table_query + line.strip() + ",\n"
            alter_table_query = alter_table_query[:-2] + ";"
            print(alter_table_query + "\n")
        

        ret = execute_sql_command(create_table_query.lower(),haveToCommit=True)
        if(ret["result"] == 1):
            if(constraint_file != None):
                ret = execute_sql_command(alter_table_query.lower(),haveToCommit=True)
        else:
            return ret

        if(ret["result"] == 1):
            values_present = False
            insert_query = f"INSERT INTO {table_name} VALUES \n"
            for row in df.itertuples():
                insert_query = insert_query + "("
                for value in row[1:]:
                    values_present = True
                    if(type(value) is not float or not math.isnan(value) ):
                        insert_query += f"'{value}', " 
                    else:
                        insert_query += f"NULL, "
                insert_query = insert_query[:-2] + "),\n"
            insert_query = insert_query[:-2] + ";"
            if(values_present):
                ret = execute_sql_command(insert_query.lower(),haveToCommit=True)
        else:
            #table created but problem with constraint
            execute_sql_command(f"DROP TABLE {table_name}",haveToCommit= True)
            ret["msg"] = "table created but problem with constraint   " + ret["msg"]
            return ret
        
        if(ret["result"] == 1):
            return execute_sql_command(f"SELECT * FROM {table_name}",fetchResults= True)
        else:
            #table created and constraint added but problem with data
            execute_sql_command(f"DROP TABLE {table_name}",haveToCommit= True)
            ret["msg"] = "table created and constraint added but problem with data   " + ret["msg"]
            return ret
    except Exception as e:
        execute_sql_command(f"DROP TABLE {table_name}",haveToCommit= True)
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
    

