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
    return getUserSpecificData(user_email,utils.PREDICTION_TABLE_NAME)

def getFullUserPredictions(user_email):
    try:
        query = f"SELECT {utils.MATCHES_TABLE_NAME}.*  ,{utils.PREDICTION_TABLE_NAME}.user_prediction  FROM {utils.PREDICTION_TABLE_NAME}"
        query = query + f"\nINNER JOIN {utils.MATCHES_TABLE_NAME}" 
        query = query + f"\nON {utils.MATCHES_TABLE_NAME}.match_id = {utils.PREDICTION_TABLE_NAME}.match_id" 
        query = query + "\nWHERE user_email =%s " 
        ret = utils.execute_sql_command(query,fetchResults=True,parameter=(user_email,))
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}
    

def addUserToUserTable(user_email,user_name,password,avatar):
    try:
        query = "INSERT INTO " + utils.USERS_TABLE_NAME + " (user_email,user_name,password,avatar) VALUES(%s,%s,%s,%s);"
        ret = utils.execute_sql_command(query,parameter=(user_email,user_name,password,avatar,),haveToCommit= True)
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}
    
def addUserToTop4Table(user_email,user_name):
    try:
            query = "INSERT INTO " + utils.TOP4_TABLE_NAME + " (user_email,user_name) VALUES(%s,%s);"
            ret = utils.execute_sql_command(query,parameter=(user_email,user_name,),haveToCommit= True)
            return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}


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
        query = f"DELETE FROM {utils.TOP4_TABLE_NAME} WHERE user_email=%s"
        ret = utils.execute_sql_command(query,parameter = (user_email,),haveToCommit= True)
        query = f"DELETE FROM {utils.PREDICTION_TABLE_NAME} WHERE user_email=%s"
        ret = utils.execute_sql_command(query,parameter = (user_email,),haveToCommit= True)
        query = f"DELETE FROM {utils.USERS_TABLE_NAME} WHERE user_email=%s"
        ret = utils.execute_sql_command(query,parameter = (user_email,),haveToCommit= True)
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}


def updateUserPredictions(user_email,predictionsList):
    try:
        print(predictionsList)
        for prediction in predictionsList:
            print(type(prediction["user_prediction"]))

            query = f"UPDATE predictions SET user_prediction = %s WHERE user_email=%s AND match_id=%s"
            print(query)
            ret = utils.execute_sql_command(query,parameter = (prediction["user_prediction"],user_email,prediction["match_id"],),haveToCommit= True)
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}


def getUserFirstTop4(user_email):
    try: 
        query = "SELECT col1,col2,col3,col4 from " + utils.TOP4_TABLE_NAME + " WHERE user_email = %s"
        ret = utils.execute_sql_command(query,parameter=(user_email,),fetchResults=True);
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}


def getUserSecondTop4(user_email):
    try: 
        query = "SELECT col5,col6,col7,col8 from " + utils.TOP4_TABLE_NAME + " WHERE user_email = %s"
        ret = utils.execute_sql_command(query,parameter=(user_email,),fetchResults=True);
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}


def updateUserTop4Poins(user_email, real_top4: list):
    try: 
        points = 0
        ret = getUserFirstTop4(user_email)
        if(ret["result"] == 1):
            first_top4_list = list(json.loads(ret["msg"])[0].values())
            ret = getUserSecondTop4(user_email)
            if(ret["result"] == 1):
                second_top4_list = list(json.loads(ret["msg"])[0].values())
            else: 
                return ret 
        else:
            return ret 

        for team in real_top4:
            if(team in first_top4_list):
                points = points + utils.TEAMS_PRESENT_IN_FIRST_TOP4_PRED
                if(real_top4.index(team) == first_top4_list.index(team)):
                    points = points + utils.TEAMS_CORRECT_POSITON_PRED_SECOND_TOP4

            if(team in second_top4_list):
                points = points + utils.TEAMS_PRESENT_IN_SECOND_TOP4_PRED
                if(real_top4.index(team) == second_top4_list.index(team)):
                    points = points + utils.TEAMS_CORRECT_POSITON_PRED_SECOND_TOP4

        query = f"UPDATE {utils.TOP4_TABLE_NAME} SET points = {points} WHERE user_email=%s"
        return utils.execute_sql_command(query,parameter=(user_email,),haveToCommit=True) 

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}


def updateUserTop4Pred(user_email,top4_prediciton_list,firstPred):
    try:
        first,second,third,fourth = top4_prediciton_list
        if(firstPred):
            query = f"UPDATE {utils.TOP4_TABLE_NAME} SET col1 = %s ,col2 = %s ,col3 = %s , col4 = %s WHERE user_email = %s"
        else:
            query = f"UPDATE {utils.TOP4_TABLE_NAME} SET col5 = %s , col6 = %s ,col7 = %s , col8 = %s WHERE user_email = %s"  
        ret = utils.execute_sql_command(query,parameter=(first,second,third,fourth,user_email),haveToCommit=True) 
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}