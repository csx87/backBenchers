import utils

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
    return getUserSpecificData(user_email,utils.USERS_TABLE_NAME)