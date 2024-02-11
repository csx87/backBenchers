import utils


def getTeams():
    try: 
        query = "SELECT * from " + utils.TEAMS_TABLE_NAME.lower() 
        ret = utils.execute_sql_command(query,True);
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}

def getMatches():
    try: 
        query = "SELECT * from " + utils.MATCHES_TABLE_NAME.lower() 
        ret = utils.execute_sql_command(query,True);
        return ret
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return {"result": 0, "msg": error_msg}
