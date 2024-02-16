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

    
def createUserPredictionTable(user_email):
    try:
        uid = user.getUserID(user_email)
        print(uid)
        if(uid != -1):
            table_name = "user_" + str(uid) + "_predictions"
            query = "CREATE TABLE " + table_name
            query = query + "(match_id INT NOT NULL, FOREIGN KEY (match_id) REFERENCES matches(match_id),"
            query = query + "user_prediction VARCHAR(255) DEFAULT NULL,FOREIGN KEY (user_prediction) REFERENCES teams(team_name));"
            ret = utils.execute_sql_command(query,haveToCommit=True) #parameter=(table_name,)
            if(ret["result"] != 1):
                user.delUserAndPredictionTable(user_email,table_name)
                return {"result":0,"msg":f"Not able to create prediction table. Please contact backend engg {ret['msg']}"}

            ret = getMatches()
            if(ret["result"] == 1):
                matchList = json.loads(ret['msg'])
                for match in matchList:
                    match_id = match["match_id"]
                    query = "INSERT INTO " + table_name + f" (match_id) VALUES({match_id})"
                    ret = utils.execute_sql_command(query,haveToCommit=True) 
                    if(ret["result"] != 1):
                        user.delUserAndPredictionTable(user_email,table_name)
                        return {"result":0,"msg":f"Not able to create prediction table. Please contact backend engg {ret['msg']}"}
            else:
                user.delUserAndPredictionTable(user_email,table_name)
                return {"result":0,"msg":f"Not able to create prediction table due to matches table. Please contact backend engg {ret['msg']}"}

            return ret

        else:
            user.delUserAndPredictionTable(user_email,table_name)
            error_msg = f"An unexpected error occurred: Didn't get valid uid"
            return {"result": 0, "msg": error_msg}
        
    except Exception as e:
        user.delUserAndPredictionTable(user_email,table_name)
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}
    

def getUserPredictionTable(user_email):
    try:
        ret = {"result":0,"msg":""}
        uid = user.getUserID(user_email)
        print(uid)
        if(uid != -1):
            table_name = "user_" + str(uid) + "_predictions"
            query = "SELECT * FROM " + table_name
            ret = utils.execute_sql_command(query,fetchResults=True) 
            if(ret["result"] != 1):
                return {"result":0,"msg":f"Not able to create prediction table. Please contact backend engg {ret['msg']}"}
            return ret 
        
        else:
            error_msg = f"User doesn't exist"
            return {"result": 0, "msg": error_msg}
        
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}


def setupTables():
    try:
        with open("tables_setup.txt", 'r') as file:
            queries = file.read().split(';')[:-1]
            for query in queries:
                ret = utils.execute_sql_command(query,haveToCommit=True)
                if(ret['result'] != 1):
                    return ret 
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


