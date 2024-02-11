from flask import Flask, request, jsonify, abort
import utils

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
    


if __name__ == '__main__':
    app.run(debug=True)
