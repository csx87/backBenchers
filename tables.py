import utils
import user
import json
import pandas as pd



def getTable(table_name):
    try: 
        query = "SELECT * from " + table_name.lower() 
        ret = utils.execute_sql_command(query,fetchResults=True);
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}

def getTeams():
    return getTable(utils.TEAMS_TABLE_NAME)

def getMatches():
    return getTable(utils.MATCHES_TABLE_NAME)
    
def getLeaderboard():
    return getTable(utils.LEADERBOARD_TABLE_NAME)
    
def getUsers():
    return getTable(utils.USERS_TABLE_NAME)

def getTop4():
    return getTable(utils.TOP4_TABLE_NAME)

    
def setupTables():
    try:
        with open("tables_setup.txt", 'r') as file:
            queries = file.read().split(';')[:-1]
            for query in queries:
                ret = utils.execute_sql_command(query,haveToCommit=True)
                if(ret["result"] != 1):
                    return ret
            return {"result":1,"msg":"Tables Created succesfully"}
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}



def check_if_user_email_exists(mail):
    try:
        #Depends on msg format
        data = json.loads(getUsers()["msg"])
        # Check if any user has the given name
        return any(element["user_email"] == mail for element in data)
    except (KeyError, json.JSONDecodeError):
        # Handle missing or invalid JSON data
        return False
    
def check_if_user_name_exists(name):
    try:
        #Depends on msg format
        data = json.loads(getUsers()["msg"])
        # Check if any user has the given name
        return any(element["user_name"] == name for element in data)
    except (KeyError, json.JSONDecodeError):
        # Handle missing or invalid JSON data
        return False


