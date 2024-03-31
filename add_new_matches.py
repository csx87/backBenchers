import sys
import user
import tables as tb
import time
import utils
import os
import json

# The first argument (sys.argv[0]) is the script name
script_name = sys.argv[0]

# The second argument (sys.argv[1]) is the excel_file_path
excel_file_path = sys.argv[1]

try :
# Open a file in write mode
 with open("output.txt", "w") as f:
    # Write the Excel file path to the file
    ret = utils.excel_to_mysql(utils.MATCHES_TABLE_NAME,excel_file_path,checkTableEmpty =False)
    os.remove(excel_file_path)
            
    if(ret["result"] == 1):

                query = f"SELECT {utils.MATCHES_TABLE_NAME}.{utils.MATCHES_ID_COL_NAME} FROM {utils.PREDICTION_TABLE_NAME} RIGHT JOIN matches ON {utils.PREDICTION_TABLE_NAME}.{utils.MATCHES_ID_COL_NAME}  = {utils.MATCHES_TABLE_NAME}.{utils.MATCHES_ID_COL_NAME} WHERE {utils.PREDICTION_TABLE_NAME}.{utils.MATCHES_ID_COL_NAME} is NULL"
                ret = utils.execute_sql_command(query,fetchResults=True)

                if(ret["result"] == 1):
                    new_matches_list = json.loads(ret['msg'])
                    match_id_list = []
                    for match in new_matches_list:
                        match_id_list.append(match["match_id"])

                    user_list = tb.getUsersList()
                    
                    for user_email in user_list:
                        ret = user.addNewMatches(user_email,match_id_list)
                        time.sleep(5)

                    if(ret["result"] != 1):
                        f.write("user.addNewMatches failed")
                        sys.exit(0)

                    else:
                        f.write("user.addNewMatches succeded")
                        sys.exit(0)

                else:
                    f.write("execute_sql_command_fail")
                    sys.exit(0)
    else:
         f.write(f"Error in excel to mysql {ret['msg']}")
         sys.exit(0)


except Exception as e:
    f.write(e)
    sys.exit(0)
