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
        if request.headers['Content-type'] != "application/json":
        	abort(401, 'Content-type should be application/json')

@app.route('/pingServer')
def ping():
    validateHeaders(FRONTEND_API_KEY)
    try:
        ret = utils.execute_sql_command("SELECT 1")
        if(ret["result"] == 1):
                return jsonify({"result": 1, "msg": "server is on and database is available"})
        else:
            return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
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
        return jsonify({"result": 0, "msg": error_msg})

@app.route('/getTop4',methods=['GET'])
def getTop4():
    validateHeaders(FRONTEND_API_KEY)
    try:
        ret = tb.getTop4()
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
          return jsonify(user.getUserPredictions(request.headers["user-email"]))
        else:
          return jsonify(ret)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg})
    
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

@app.route('/setupTables',methods=['GET'])
def setupTables():
    try:
       validateHeaders(BACKEND_API_KEY)
       ret = tb.setupTables()
       return ret 
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500


#------------------------------------------------------------------POST METHODS--------------------------------------------------------------------------#
@app.route('/addUser',methods=['POST'])
def addUser():
    try:
        #------------------ Validating Headers and payload -------------------------------------------#
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
        
        # Adding the corresponding matches for user in prediction table
        if(ret['result'] == 1):
            ret = tb.createUserPredictionTable(email)
            if(ret["result"] != 1):
                return ret


        #if user is added to both user and match table then return or else delete the user
        if(ret["result"] == 1):
          return jsonify(user.getUserInfo(email));

        
        if(ret!=None):
          return jsonify(ret)
        else:
            error_msg = f"An unexpected error occurred: NULL"
            return jsonify({"result": 0, "msg": error_msg}), 500
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 1, "msg": error_msg}), 500


@app.route('/addTable',methods=['POST'])
def addTable():
    try:
        excel_file_path = ""
        constraints_file_filename = ""

        validateHeaders(BACKEND_API_KEY)
        constraints_file_present = False
        if 'table-name' not in request.headers:
            return jsonify({"result": 1, "msg": "table_name not found in headers "}), 500
        table_name = request.headers["table-name"]

        if 'excel-file' not in request.files:
            return jsonify({"result": 1, "msg": "No excel or ods file found"}), 500
        
        if 'constraints-file' in request.files:
            constraints_file_present = True

        excel_file = request.files["excel-file"]

        if(constraints_file_present):
            constraints_file = request.files["constraints-file"]


        if(excel_file.filename == ""):
            return jsonify({"result": 1, "msg": "The excel/ods file provided is not proper"}), 500
        
        if excel_file:
            excel_file_path = f'tables/{table_name}_{excel_file.filename}'
            excel_file.save(excel_file_path)
        
        if(constraints_file_present == True and constraints_file.filename != ""):
            constraints_file_filename = f'tables/{table_name}_{constraints_file.filename}'
            constraints_file.save(constraints_file_filename)
        
        if(constraints_file_present):
            ret = utils.excel_to_mysql(table_name,excel_file_path,constraints_file_filename)
        
        else:
            ret = utils.excel_to_mysql(table_name,excel_file_path,None)

        if excel_file:
            os.remove(excel_file_path)

        if(constraints_file_present and constraints_file):
            os.remove(constraints_file_filename)
        

        return ret  

    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return jsonify({"result": 0, "msg": error_msg}), 500





if __name__ == '__main__':
    app.run(debug=True)