from flask import Flask, request, jsonify, abort
import utils
import tables as tb
import user

app = Flask(__name__)

# MySQL configurations
config = utils.config
BACKEND_API_KEY = utils.BACKEND_API_KEY
FRONTEND_API_KEY = utils.FRONTEND_API_KEY


def validateHeaders(API_KEY, is_post = False):
    if 'api-key' not in request.headers:
            abort(401, 'Missing API key')
    
        # Verify the API key
    if request.headers['api-key'] != API_KEY:
        	abort(401, 'Invalid API key')
              
    if(is_post):
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



if __name__ == '__main__':
    app.run(debug=True)
