import utils
import json
import tables as tb

def getUserSpecificData(user_email,table_name):
    try:
        query = "SELECT * from " + table_name + " " + "WHERE user_email=%s"
        ret = utils.execute_sql_command(query,True,(user_email,))
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}

def getUserInfo(user_email):
    return getUserSpecificData(user_email,utils.USERS_TABLE_NAME)
    
def getUserPredictions(user_email):
    return tb.getUserPredictionTable(user_email)

def addUserToUserTable(user_email,user_name,password,avatar):
    try:
        query = "INSERT INTO " + utils.USERS_TABLE_NAME + " (user_email,user_name,password,avatar) VALUES(%s,%s,%s,%s);"
        ret = utils.execute_sql_command(query,parameter=(user_email,user_name,password,avatar,),haveToCommit= True)
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}
    
def addUserToLeaderboardTable(user_email):
    try:
        user_id = getUserID(user_email)
        if(user_id >0):
            query = "INSERT INTO " + utils.LEADERBOARD_TABLE_NAME + " (user_id) VALUES(%s);"
            ret = utils.execute_sql_command(query,parameter=(user_id,),haveToCommit= True)
            return 
        else:
            return {"result": 0, "msg": "Couldn't Insert to leadreboard"}
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}

def getUserID(user_email):
    try:
        query = "SELECT user_id FROM " + utils.USERS_TABLE_NAME + " WHERE user_email = %s"
        ret = utils.execute_sql_command(query,parameter=(user_email,),fetchResults=True)
        return json.loads(ret['msg'])[0]["user_id"]
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return -1
    

def delUserAndPredictionTable(user_email,user_table):
    try:
        ret = None
        query = "DROP TABLE IF EXISTS " + user_table 
        ret = utils.execute_sql_command(query,haveToCommit= True)
        query = "DELETE FROM users WHERE user_email=%s"
        ret = utils.execute_sql_command(query,parameter=(user_email,),haveToCommit= True)
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}

    

