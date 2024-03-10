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


def getUsers():
    return getTable(utils.USERS_TABLE_NAME)

def getTop4():
    return getTable(utils.TOP4_TABLE_NAME)
    
def getLeaderboard():
    try:
        matches_won = "SUM(CASE WHEN (matches.team_won = predictions.user_prediction AND matches.team_won IS NOT NULL) THEN 1 ELSE 0 END)"
        matches_lost = "SUM(CASE WHEN (matches.team_won != predictions.user_prediction AND matches.team_won IS NOT NULL) THEN 1 ELSE 0 END)"
        matches_not_predicted = "SUM(CASE WHEN (matches.team_won IS NOT NULL AND predictions.user_prediction is NULL) THEN 1 ELSE 0 END)"

        points = f"{matches_won}*{utils.MATCHES_WON_POINT} + {matches_lost}*{utils.MATCHES_LOST_POINT} + {matches_not_predicted}*{utils.MATCHES_NOT_PREDICTED_POINT}"

        table = f"FROM {utils.PREDICTION_TABLE_NAME}\n"
        table = table + f"INNER JOIN {utils.MATCHES_TABLE_NAME}\n"
        table = table + f"ON {utils.MATCHES_TABLE_NAME}.{utils.MATCHES_ID_COL_NAME} = {utils.PREDICTION_TABLE_NAME}.{utils.MATCHES_ID_COL_NAME}\n"

        cond = "WHERE start_time < DATE_ADD(DATE_ADD(NOW(), INTERVAL 5 HOUR), INTERVAL 30 MINUTE)\n"
        cond = cond + "GROUP BY user_name ORDER BY points DESC;"

        query = f"SELECT user_name, {matches_won} as matches_won, {matches_lost} as matches_lost, {matches_not_predicted} as matches_not_predicted, {points} as points\n"
        query = query + table + cond

        return utils.execute_sql_command(query,fetchResults=True)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}
    


    
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


