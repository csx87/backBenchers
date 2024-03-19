
## Setting up the database
1) Install my_sql

i) `` sudo apt install mysql-server ``
ii) ``sudo systemctl start mysql.service``

2) Configure my-sql

i) ``sudo mysql``

Then run the following `ALTER USER` command to change the **root** user’s authentication method to one that uses a password. The following example changes the authentication method to `mysql_native_password`:

ii) ``ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';``

3) Create a database

i) ``mysql -u root -p``
ii) ``CREATE DATABASE <database_name>; ``


## CONFIGURING THE SERVER

1) Clone the repository using
``git clone``

2) In utils.py 
You can change the fields appropriately 

config = {
'user': 'root',
'password': <password>,
'host': 'localhost',
'database': <database_name>
}

BACKEND_API_KEY =  <backend_api_key>
FRONTEND_API_KEY =  <frontend_api_key>

MATCHES_WON_POINT =  2
MATCHES_LOST_POINT =  0
MATCHES_NOT_PREDICTED_POINT =  -1

TEAMS_PRESENT_IN_FIRST_TOP4_PRED =  3
TEAMS_CORRECT_POSITON_PRED_FIRST_TOP4 =  3
TEAMS_PRESENT_IN_SECOND_TOP4_PRED =  2
TEAMS_CORRECT_POSITON_PRED_SECOND_TOP4 =  2 

## LAUNCHING THE SERVER


1) Use the virtual env provided to run the server:
	i) `` source venv/bin/activate ``
	ii) ``python3 -m flask_server.py``

Optional : If the venv provided doesn't work you can create your own virtual env and install the necessary plugins 
			i) Create venv :
			``python3 -m venv venv``
			ii)  Activate the venv:
			``pip install -U Flask``
			iii) Installing plugins:
			 -> Flask : ``pip install -U Flask``
			 -> *mysql_connector-python*: ```pip install mysql-connector-python```
			 -> pandas : ``pip install pandas``
			 -> gunicorn : ``pip3 install gunicorn``

2) Execute pingServer  curl call using:
``curl --location 127.0.0.1:8001/pingServer --header 'api-key: <frontend_api_key>'``

 If everything went correct you should receive this message;

`` server is on and database is available``


## DEPLOYING SERVER
1) Run gunicorn :

``gunicorn --bind 0.0.0.0:8000 flask_server:app``

The following shows gunicorn working successfully :
``
[2021–01–07 14:29:30 +0000] [1288] [INFO] Starting gunicorn 20.0.4   
[2021–01–07 14:29:30 +0000] [1288] [INFO] Listening at: [http://127.0.0.1:8000](http://127.0.0.1:8000) (1288)   
[2021–01–07 14:29:30 +0000] [1288] [INFO] Using worker: sync   
[2021–01–07 14:29:30 +0000] [1291] [INFO] Booting worker with pid: 1291
``

 Execute pingServer  curl call using:
``curl --location 127.0.0.1:8000/pingServer --header 'api-key: <frontend_api_key>'``
Note: I have changed the port number to 8000 form 8001 

 If everything went correct you should receive this message;
`` server is on and database is available``

2) Create a systemd Unit file:

Instead of running the flask app using the command above, we can create a service so that Ubuntu can automatically run the flask app with gunicorn upon booting. This step will be done using systemd.

``sudo vi /etc/systemd/system/<service_name>.service``

Copy the following lines: 

[Unit]
Description=Gunicorn instance for a simple hello world app
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=<path_to_server_dir>
ExecStart=sudo <path_to_server_dir>/venv/bin/gunicorn -b localhost:8000 flask_server:app
Restart=always
[Install]
WantedBy=multi-user.target



``sudo systemctl daemon-reload``
`` sudo systemctl start <service_name>``
``sudo systemctl enable <service_name>``

Execute pingServer  curl call using:
``curl --location 127.0.0.1:8000/pingServer --header 'api-key: <frontend_api_key>'``


 If everything went correct you should receive this message;
`` server is on and database is available``

3) Install nginx and configure it
``sudo apt-get install nginx``
``sudo systemctl start nginx``
``sudo systemctl enable nginx``

copy the contens of nginx_configure.txt:
``sudo cp nginx_configure.txt /etc/nginx/sites-available/default``
``sudo systemctl restart nginx``

Now all the RestEndPoints will be available for you to use


## CREATING TABLES

Refer the backend_api_calls
i) Call the setUpTables
ii) Call populateTeamsTable
iii) Call populateMatchesTable

Now server is fully ready for handling any requests from the frontend


