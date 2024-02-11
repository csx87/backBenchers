import utils

def getTable(table_name):
    try: 
        query = "SELECT * from " + table_name.lower() 
        ret = utils.execute_sql_command(query,True);
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