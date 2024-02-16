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
    
def addUserToLeaderboardTable(user_email,user_name):
    try:
            query = "INSERT INTO " + utils.LEADERBOARD_TABLE_NAME + " (user_email,user_name) VALUES(%s,%s);"
            ret = utils.execute_sql_command(query,parameter=(user_email,user_name,),haveToCommit= True)
            return ret
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

def addUserToPredictionTable(user_email,user_name):
    try:
            table_name = utils.PREDICTION_TABLE_NAME
            ret = tb.getMatches()
            if(ret["result"] == 1):
                matchList = json.loads(ret['msg'])
                for match in matchList:
                    match_id = match["match_id"]
                    query = "INSERT INTO " + table_name + f" (match_id,user_email,user_name) VALUES({match_id},%s,%s)"
                    ret = utils.execute_sql_command(query,parameter=(user_email,user_name,),haveToCommit=True) 
                    if(ret["result"] != 1):
                        delUser(user_email,table_name)
                        return {"result":0,"msg":f"Not able to create prediction table. Please contact backend engg {ret['msg']}"}
                return ret
            else:
                delUser(user_email,table_name)
                return {"result":0,"msg":f"Not able to create prediction table due to matches table. Please contact backend engg {ret['msg']}"}
            
    except Exception as e:
        delUser(user_email,table_name)
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}

def delUser(user_email):
    try:
        ret = None
        query = f"DELETE FROM {utils.LEADERBOARD_TABLE_NAME} WHERE user_email=%s"
        ret = utils.execute_sql_command(query,(user_email,),haveToCommit= True)
        query = f"DELETE FROM {utils.PREDICTION_TABLE_NAME} WHERE user_email=%s"
        ret = utils.execute_sql_command(query,(user_email,),haveToCommit= True)
        query = f"DELETE FROM {utils.USERS_TABLE_NAME} WHERE user_email=%s"
        ret = utils.execute_sql_command(query,(user_email,),haveToCommit= True)
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}