from flask import Flask, request, jsonify, abort
import utils
import tables as tb
import user
import os

app = Flask(__name__)

# MySQL configurations
config = utils.config
BACKEND_API_KEY = utils.BACKEND_API_KEY
FRONTEND_API_KEY = utils.FRONTEND_API_KEY


def validateHeaders(API_KEY, check_json_content = False):
        if 'api-key' not in request.headers:
                abort(401, 'Missing API key')
        
            # Verify the API key
        if request.headers['api-key'] != API_KEY:
                abort(401, 'Invalid API key')
                
        if(check_json_content):
            if 'Content-type' not in request.headers:
                abort(401, 'Missing Content-type')
        
            # Verify the API key
            if 'application/json' not in request.headers['Content-Type']:
                print(request.headers['Content-Type'])
                abort(401, 'Content-type should be application/json')


@app.route('/pingServer')
def ping():
    try:
        validateHeaders(FRONTEND_API_KEY)
        ret = utils.execute_sql_command("SELECT 1")
        if(ret["result"] == 1):
                return jsonify({"result": 1, "msg": "server is on and\ database is available"})
        else:
            return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred : {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})
    
@app.route('/getTeams',methods=['GET'])
def getTeams():
    validateHeaders(FRONTEND_API_KEY)
    try:
        ret = tb.getTeams()
        return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})
    
@app.route('/getMatches',methods=['GET'])
def getMatches():
    validateHeaders(FRONTEND_API_KEY)
    try:
        ret = tb.getMatches()
        return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})

@app.route('/getUsers',methods=['GET'])
def getUsers():
    validateHeaders(FRONTEND_API_KEY)
    try:
        ret = tb.getUsers()
        return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})
    
@app.route('/getLeaderboard',methods=['GET'])
def getLeaderboard():
    validateHeaders(FRONTEND_API_KEY)
    try:
        ret = tb.getLeaderboard()
        return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": -1, "msg": error_msg})

@app.route('/getTop4',methods=['GET'])
def getTop4():
    validateHeaders(FRONTEND_API_KEY)
    try:
        ret = tb.getTop4()
        return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})    

@app.route('/getUserFirstTop4',methods=['GET'])
def getUserFirstTop4():
    validateHeaders(FRONTEND_API_KEY)
    try:
        if 'user-email' not in request.headers:
            abort(401, 'Missing user-email')
        if 'password' not in request.headers:
            abort(401, 'Missing password')
    
        ret = utils.checkPassword(request.headers["user-email"],request.headers["password"])

        if(ret["result"] == 1):
          return jsonify(user.getUserFirstTop4(request.headers["user-email"]))
        else:
          return jsonify(ret)

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})

@app.route('/getUserSecondTop4',methods=['GET'])
def getUserSecondTop4():
    validateHeaders(FRONTEND_API_KEY)
    try:
        if 'user-email' not in request.headers:
            abort(401, 'Missing user-email')
        if 'password' not in request.headers:
            abort(401, 'Missing password')
    
        ret = utils.checkPassword(request.headers["user-email"],request.headers["password"])

        if(ret["result"] == 1):
          return jsonify(user.getUserSecondTop4(request.headers["user-email"]))
        else:
          return jsonify(ret)

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})     

    
@app.route('/getUserInfo',methods=['GET'])
def getUserInfo():
    try:
        validateHeaders(FRONTEND_API_KEY)
        if 'user-email' not in request.headers:
            abort(401, 'Missing user-email')
        if 'password' not in request.headers:
            abort(401, 'Missing password')
    
        ret = utils.checkPassword(request.headers["user-email"],request.headers["password"])
    
        if(ret["result"] == 1):
          return jsonify(user.getUserInfo(request.headers["user-email"]))
        else:
          return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})
    
@app.route('/getUserPredictions',methods=['GET'])
def getUserPredictions():
    try:
        validateHeaders(FRONTEND_API_KEY)
        if 'user-email' not in request.headers:
            abort(401, 'Missing user-email')
        if 'password' not in request.headers:
            abort(401, 'Missing password')
    
        ret = utils.checkPassword(request.headers["user-email"],request.headers["password"])

    
        if(ret["result"] == 1):
          return jsonify(user.getFullUserPredictions(request.headers["user-email"]))
        else:
          return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})

'''  
@app.route('/updateUserPredictions',methods=['GET'])
def updateUserPredictions():
    try:
        validateHeaders(FRONTEND_API_KEY)
        if 'user-email' not in request.headers:
            abort(401, 'Missing user-email')
        if 'password' not in request.headers:
            abort(401, 'Missing password')
    
        ret = utils.checkPassword(request.headers["user-email"],request.headers["password"])
        
    
        if(ret["result"] == 1):
          return jsonify(user.updateUserPredictions(request.headers["user-email"]))
        else:
          return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})
'''

@app.route('/setupTables',methods=['POST'])
def setupTables():
    try:
       validateHeaders(BACKEND_API_KEY)
       ret = tb.setupTables()
       return jsonify(ret) 
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500


#------------------------------------------------------------------POST METHODS--------------------------------------------------------------------------#
@app.route('/addUser',methods=['POST'])
def addUser():
    try:
        #------------------ Validating Headers and payload -------------------------------------------#
        email = None
        validateHeaders(FRONTEND_API_KEY, check_json_content= True)
        data = request.json
        ret = None
        if "user_email" not in data.keys():
            return jsonify({"result": 0, "msg": "user_email needed"})
        if "user_name" not in data.keys():
            return jsonify({"result": 0, "msg": "user_name needed"})
        if "password" not in data.keys():
            return jsonify({"result": 0, "msg": "password is needed"})
        if "avatar" not in data.keys():
            return jsonify({"result": 0, "msg": "link to avatar is needed"})
        
        email = data["user_email"]
        name = data["user_name"]
        password = data["password"]
        avatar = data["avatar"]
        #----------------------------------------------------------------------------------------------#


        #------------------ Check valid payload data -------------------------------------------#
        if(utils.check_if_valid_user(email)):
            if(not tb.check_if_user_email_exists(email)):
                if(not tb.check_if_user_name_exists(name)):
                    if(len(password) > 8):
                        ret = user.addUserToUserTable(email,name,password,avatar)
                    else:
                        return jsonify({"result":0,"msg":"Length of password should be greater than 8"})
                else:
                    return jsonify({"result":0,"msg":"Username exists please use a different one"})
            else:
                return jsonify({"result":0,"msg":"Account already exists with the mail"})
        else:
            return jsonify({"result":0,"msg":"You are not allowed to partcipate. Please check your email or contact backend engg"})
        #----------------------------------------------------------------------------------------#
        
        if(ret['result'] == 1):
            ret = user.addUserToTop4Table(email,name)
            if(ret ["result"] == -1):
                if(email != None):
                    ret = user.delUser(email)
                    return jsonify({"result":-1,"msg":"Couldn't Add user to leadrboard deleting the user please try to add him again"})

        # Adding the corresponding matches for user in prediction table
        if(ret['result'] == 1):
            ret = user.addUserToPredictionTable(email,name)
            if(ret["result"] != 1):
                return ret

        return jsonify(user.getUserInfo(email))
        
    except Exception as e:
        error_msg = e
        try:
            if(email != None):
                ret = user.delUser(email)
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            return jsonify({"result": 0, "msg": error_msg}), 500
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500
    




@app.route('/populateTeamsTable',methods=['POST'])
def populateTeamsTable():
    try:
        table_name = utils.TEAMS_TABLE_NAME
        

        validateHeaders(BACKEND_API_KEY)

        if 'excel-file' not in request.files:
            return jsonify({"result": 1, "msg": "No excel or ods file found"}), 500
        

        excel_file_path = ""
        excel_file = request.files["excel-file"]


        if(excel_file.filename == ""):
            return jsonify({"result": 1, "msg": "The excel/ods file provided is not proper"}), 500
        
        if excel_file:
            excel_file_path = f'{table_name}_{excel_file.filename}'
            excel_file.save(excel_file_path)
            ret = utils.excel_to_mysql(table_name,"/home/ubuntu/backBenchers/teams_teams.ods")
            return jsonify(ret)
            #os.remove(excel_file_path)

        else:
            return jsonify({"result": 0, "msg": "Cannot open excel file"}), 500
        

        return ret  

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500
    

@app.route('/populateMatchesTable',methods=['POST'])
def populateMatchesTable():
    try:
        table_name = utils.MATCHES_TABLE_NAME
        excel_file_path = ""

        validateHeaders(BACKEND_API_KEY)

        if 'excel-file' not in request.files:
            return jsonify({"result": 1, "msg": "No excel or ods file found"}), 500
        

        excel_file = request.files["excel-file"]


        if(excel_file.filename == ""):
            return jsonify({"result": 1, "msg": "The excel/ods file provided is not proper"}), 500
        
        if excel_file:
            excel_file_path = f'{table_name}_{excel_file.filename}'
            excel_file.save(excel_file_path)
            ret = utils.excel_to_mysql(table_name,excel_file_path)
            return jsonify(ret)
            #os.remove(excel_file_path)

        else:
            return jsonify({"result": 0, "msg": "Cannot open excel file"}), 500
        

        return ret  

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500


@app.route('/updateUserPredictions',methods=['POST'])
def updateUserPredictions():
    try:
        validateHeaders(FRONTEND_API_KEY)

        if 'user-email' not in request.headers:
            abort(401, 'Missing user-email')
        if 'password' not in request.headers:
            abort(401, 'Missing password')

        ret = utils.checkPassword(request.headers["user-email"],request.headers["password"])
        if(ret["result"] != 1):
          return jsonify(ret)

        #data is list of dict
        data = request.json
        cont = utils.check_if_field_persent_in_list_of_dict(data,["match_id","user_prediction"])
        if(not cont):
            error_msg = """An unexpected error occurred: The json body is not of the proper format [{"match_id":"1","user_prediction":"RCB"},{"match_id":"2","user_prediction":"MI"},.....]"""
            return jsonify({"result": 0, "msg": error_msg}), 500

        ret = user.updateUserPredictions(request.headers["user-email"],data)

        if(ret["result"] == 1):
            ret = user.getFullUserPredictions(request.headers["user-email"])

        return jsonify(ret)
        
        

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500

@app.route('/updateTeamWon',methods=['POST'])
def updateTeamWon() :
    try: 
        validateHeaders(BACKEND_API_KEY,check_json_content = True)
        data = request.json

        print(type(data),data)

        if("match_id" not in data.keys() or "team_won" not in data.keys()):
            return jsonify({"result": 0, "msg": "Either match_id or team_won fields not present"}), 400

        match_id = data["match_id"]
        team_won = data["team_won"]
        if(team_won == None):
            query = f"UPDATE {utils.MATCHES_TABLE_NAME} SET team_won is NULL WHERE match_id = {match_id}"
        elif( match_id<1 or len(team_won) < 1):
            return jsonify({"result": 0, "msg": "Value for either of the field is missing or imporper"}), 400

        query = f"UPDATE {utils.MATCHES_TABLE_NAME} SET team_won = %s WHERE match_id = {match_id}"
        return jsonify(utils.execute_sql_command(query,parameter=(team_won,),haveToCommit=True))

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500


@app.route('/updateUserFirstTop4Pred',methods=['POST'])
def updateUserFirstTop4Pred():
    try: 
        validateHeaders(FRONTEND_API_KEY,check_json_content = True)
        data = request.json

        if 'user-email' not in request.headers:
                abort(401, 'Missing user-email')
        if 'password' not in request.headers:
                abort(401, 'Missing password')

        ret = utils.checkPassword(request.headers["user-email"],request.headers["password"])
        if(ret["result"] != 1):
            return jsonify(ret)

        if("team1" not in data.keys() or "team2" not in data.keys() or"team3" not in data.keys() or"team4" not in data.keys()):
                return jsonify({"result": 0, "msg": "Either team1,team2,team3,team4 fields not present"}), 400

        top4_predicted = list(data.values())

        ret = user.updateUserTop4Pred(request.headers["user-email"],top4_predicted,firstPred=True)

        return jsonify(ret)

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500   


@app.route('/updateUserSecondTop4Pred',methods=['POST'])
def updateUserSecondTop4Pred():
    try: 
        validateHeaders(FRONTEND_API_KEY,check_json_content = True)
        data = request.json

        if 'user-email' not in request.headers:
                abort(401, 'Missing user-email')
        if 'password' not in request.headers:
                abort(401, 'Missing password')

        ret = utils.checkPassword(request.headers["user-email"],request.headers["password"])
        if(ret["result"] != 1):
            return jsonify(ret)

        if("team1" not in data.keys() or "team2" not in data.keys() or"team3" not in data.keys() or"team4" not in data.keys()):
                return jsonify({"result": 0, "msg": "Either team1,team2,team3,team4 fields not present"}), 400

        top4_predicted = list(data.values())

        ret = user.updateUserTop4Pred(request.headers["user-email"],top4_predicted,firstPred=False)

        return jsonify(ret)

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500   


@app.route('/updateTop4',methods=['POST'])
def updateTop4():
    try: 
        validateHeaders(BACKEND_API_KEY,check_json_content = True)
        data = request.json

        print(type(data),data)

        if("team1" not in data.keys() or "team2" not in data.keys() or"team3" not in data.keys() or"team4" not in data.keys()):
            return jsonify({"result": 0, "msg": "Either team1,team2,team3,team4 fields not present"}), 400

        top4_result = list(data.values())

        user_list = tb.getUsersList()

        # user -> user_email
        for user_email in user_list:
            ret = user.updateUserTop4Poins(user_email,top4_result)
    
        return tb.getTop4Points()
            
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500

@app.route('/delUser',methods=['POST'])
def delUser():
    try:
        validateHeaders(FRONTEND_API_KEY)

        user_email = request.headers["user-email"]

        if(user_email in utils.VALID_USERS):
            return jsonify(user.delUser(user_email))

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500


if __name__ == '__main__':
    app.run(debug=True,port = 8001)
