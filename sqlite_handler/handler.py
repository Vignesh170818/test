import json
from logger_utils.get_logger import get_logger
import sqlite3
import os
import traceback
import pandas as pd
from datetime import datetime, timedelta
import time


# TEMP_DB_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sqlite_dbs')
logger = get_logger("database_log")

TEMP_DB_FOLDER=os.path.join("/home/LogFiles", "sqlite_dbs_core_10004024_1100")


def get_db_connection():
    db_path = os.path.join(TEMP_DB_FOLDER, 'data.db')
    connection = sqlite3.connect(db_path, timeout=15)
    return connection

def manage_connection(func):
    """decorator method for handling exceptions and closing connection.
    This mitigates connection to table being hung"""
    def wrapper(*args, **kwargs):
        connection=get_db_connection()
        try:
            return func(connection=connection,*args, **kwargs)
        except Exception as e:
            import inspect, sys
            cf = inspect.currentframe().f_back
            cm = cf.f_code.co_name
            cl = cf.f_lineno
            cfn = cf.f_globals['__file__']
            caller_dict={"Calling method:":cm,"Calling line number:":cl,"Calling file name:":cfn}
            logger.error(f"\n\nError occured while performing db operation.\nError:{e}\nCaller_details:{caller_dict} ...\nClosing connection")
            connection.close()
            return False
        
    wrapper.__name__ = func.__name__
    return wrapper


def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_dtobj(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')


# Function to check if the database file exists
def is_database_present():
    db_path = os.path.join(TEMP_DB_FOLDER, 'data.db')
    return os.path.exists(db_path)

# Function to create a new database and tables required
@manage_connection
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user_requests (id INTEGER PRIMARY KEY,\
                    request_id TEXT,\
                    session_id TEXT,\
                    status TEXT,  \
                    status_reason TEXT ,\
                    created_on TEXT DEFAULT CURRENT_TIMESTAMP,\
                    modified_on TEXT DEFAULT CURRENT_TIMESTAMP,\
                    created_by TEXT,\
                    file_content TEXT, \
                    epic_checksum TEXT, \
                    feature_checksum TEXT,\
                    userstories_checksum TEXT\
                    )')
    
    cursor.execute('CREATE TABLE IF NOT EXISTS tool_requests (id INTEGER PRIMARY KEY,\
                    user_request_id TEXT,\
                    tool_request_id TEXT,  \
                    tool_code TEXT, \
                    tool_request TEXT ,\
                    tool_response,\
                    entity_type,\
                    status,\
                    status_reason TEXT ,\
                    created_on TEXT DEFAULT CURRENT_TIMESTAMP, \
                    modified_on TEXT DEFAULT CURRENT_TIMESTAMP\
                    )')
    
    connection.commit()
    connection.close()



# Function to insert tool_requests into the  tool_requests table
@manage_connection        
def insert_tool_request(user_request_id, tool_request_id,tool_code, tool_request,entity_type,tool_response = None, connection=None):
    cursor = connection.cursor()
    current_timestamp = get_current_timestamp()
    tool_request = json.dumps(tool_request)
    tool_response = json.dumps({}) if tool_response == None else tool_response
    status = "NEW"
    status_reason = json.dumps({})
    cursor.execute('INSERT INTO tool_requests (user_request_id, tool_request_id, tool_code, tool_request, tool_response, entity_type, status, status_reason,created_on, modified_on) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_request_id,\
    tool_request_id,tool_code,tool_request,tool_response,entity_type,status,status_reason,current_timestamp,current_timestamp))
    connection.commit()
    connection.close()
    return True


@manage_connection
def insert_user_request(request_id,file_content,status="NEW",epic_checksum=None,feature_checksum=None,us_checksums=None, connection=None):
    cursor = connection.cursor()
    current_timestamp = get_current_timestamp()
    status = status
    status_reason = json.dumps({})
    created_by = "SYSTEM"
    file_data=file_content
    us_checksums = json.dumps([]) if us_checksums==None else us_checksums
    cursor.execute('INSERT INTO user_requests (request_id, status,status_reason,created_on,modified_on,created_by,file_content,epic_checksum,feature_checksum,userstories_checksum) VALUES (?,?, ?,?,?, ?, ?, ?,?,?)' ,(request_id,status,status_reason,current_timestamp,current_timestamp,created_by,file_data,epic_checksum,feature_checksum,us_checksums))
    connection.commit()
    connection.close()
    return True


@manage_connection
def retrieve_user_request(user_request_id, connection=None):
    cursor = connection.cursor()  
    cursor.execute('SELECT * FROM user_requests WHERE request_id = (?)',[user_request_id])
    row = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    connection.close()
    if row: 
        data  = dict(zip(column_names,row[0]))
        return data
    else:
        return None

@manage_connection
def retrieve_user_request_for_session(user_request_id, connection=None):
        
    cursor = connection.cursor()  
   
    cursor.execute('SELECT * FROM user_requests WHERE request_id = (?) and status=(?)',(user_request_id,"BUILD"))
    row = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    connection.close()
    if row: 
        data  = dict(zip(column_names,row[0]))
        return data
    else:
        return None


@manage_connection
def retrieve_user_request_for_merge(user_request_id, connection=None):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user_requests WHERE request_id = (?) and status=(?)',(user_request_id,"BUILD"))
    row = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    if row: 
        connection.close()
        data  = dict(zip(column_names,row[0]))
        return True, data
    else:
        cursor.execute('SELECT request_id FROM user_requests WHERE status=(?)',("BUILD",))
        data = cursor.fetchall()
        connection.close()
        return False, data


@manage_connection
def retrieve_file_content_by_session_id(session_id, connection=None):
    cursor = connection.cursor()  
    cursor.execute('SELECT * FROM user_requests WHERE session_id = (?) and status=(?)',(session_id,"BUILD"))
    row = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    connection.close()
    if row: 
        data  = dict(zip(column_names,row[0]))
        return data
    else:
        return None
    

@manage_connection    
def update_user_request(request_id,file_content=None,status=None,status_reason='',epic_checksum=None,feature_checksum=None,us_checksum=None, connection=None):

    cursor = connection.cursor()
    request_data = retrieve_user_request(request_id)
    file_content = request_data['file_content'] if file_content==None else file_content
    epic_checksum = request_data['epic_checksum'] if epic_checksum==None else epic_checksum
    feature_checksum = request_data['feature_checksum'] if feature_checksum==None else feature_checksum
    update_status =  request_data['status'] if status==None else status
    update_status_reason = request_data['status_reason'] if status_reason==None else request_data['status_reason'] + '\n' + status_reason 
    us_checksum = request_data['userstories_checksum'] if us_checksum==None else us_checksum
    current_timestamp = get_current_timestamp()
    if status == "COMPLETED":
        del_tool_request_by_userrequestid(request_id)
        file_content = ""        
    cursor.execute('UPDATE user_requests SET file_content=?,epic_checksum=?,feature_checksum=?,status=?, status_reason=?,\
    userstories_checksum=?,\
    modified_on=? WHERE request_id=?', (file_content,epic_checksum,feature_checksum,update_status,\
    update_status_reason,us_checksum,current_timestamp,request_id))

    connection.commit()
    connection.close()
    return True
    
@manage_connection
def retrieve_new_user_requests(connection=None):
    cursor = connection.cursor()  
    cursor.execute('SELECT * FROM user_requests WHERE status = (?)',["NEW"])
    rows = cursor.fetchall()
    if len(rows) == 0:
        return rows
    column_names = [description[0] for description in cursor.description]
    connection.close()
    data = []
    for row in rows:
        data.append(dict(zip(column_names,row)))
    return data

@manage_connection
def retrieve_tool_request(user_request_id, tool_request_id, connection=None):

    cursor = connection.cursor()  
    cursor.execute('SELECT * FROM tool_requests WHERE user_request_id = (?) and tool_request_id= (?)',(user_request_id, tool_request_id))
    row = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    connection.close() 
    if row:
        data  = dict(zip(column_names,row[0]))
    else:
        data = "no data found"
    return data

@manage_connection
def retrieve_tool_request_by_user_request_id(user_request_id, connection=None):
    cursor = connection.cursor()  
    cursor.execute('SELECT * FROM tool_requests WHERE user_request_id = (?)',(user_request_id,))
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    connection.close()
    data = []
    if rows:
        for row in rows:
            data.append(dict(zip(column_names,row)))
    else:
        data = "no data found"
    return data

@manage_connection
def update_tool_request(user_request_id,tool_request_id,status=None,status_reason=None,tool_response=None, connection=None):
    cursor = connection.cursor()
    request_data = retrieve_tool_request(user_request_id, tool_request_id)
    update_status =  request_data['status'] if status==None else status
    update_status_reason = request_data['status_reason'] if status_reason==None else status_reason
    update_tool_response = request_data['tool_response'] if tool_response==None else tool_response
    current_timestamp = get_current_timestamp()

    cursor.execute('UPDATE tool_requests SET tool_response=?, status=?, status_reason=?, modified_on=? WHERE user_request_id=? and tool_request_id=?', (update_tool_response,update_status,\
    update_status_reason,current_timestamp,user_request_id, tool_request_id))

    connection.commit()
    connection.close()
    return True

@manage_connection
def get_latest_user_request_id(connection=None):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_requests WHERE DATE(created_on) = DATE('now') ORDER BY created_on DESC LIMIT 1")
    rows = cursor.fetchall()
    connection.close()
    data = []
    column_names = [description[0] for description in cursor.description]
    if rows:
        for row in rows:
            data.append(dict(zip(column_names,row)))
    return data
    
@manage_connection
def retrieve_all_user_requests(connection=None):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_requests WHERE DATE(created_on) = DATE('now') ORDER BY created_on DESC")
    requests = cursor.fetchall()

    connection.close()
    return requests


@manage_connection
def retrieve_all_tool_requests(connection=None):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tool_requests WHERE DATE(created_on) = DATE('now') ORDER BY created_on DESC")
    requests = cursor.fetchall()

    connection.close()
    return requests

@manage_connection
def retrive_user_request_by_status(status, connection=None):
    
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user_requests WHERE status=? ORDER BY created_on DESC', (status,))
    requests = cursor.fetchall()

    connection.close()
    return requests


@manage_connection
def retrive_tool_request_by_status(status, connection=None):

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tool_requests WHERE status=? ORDER BY created_on DESC', (status,))
    requests = cursor.fetchall()

    connection.close()
    return requests


@manage_connection
def del_user_request(num_of_days=1, connection=None):
    cursor = connection.cursor()    
    threshold_date = datetime.now() - timedelta(days=num_of_days)
    cursor.execute('DELETE FROM user_requests WHERE modified_on < ?', (threshold_date,))

    connection.commit()
    connection.close()


@manage_connection
def del_tool_request(num_of_days=1, connection=None):

    cursor = connection.cursor()    
    threshold_date = datetime.now() - timedelta(days=num_of_days)
    cursor.execute('DELETE FROM tool_requests WHERE modified_on < ?', (threshold_date,))

    connection.commit()
    connection.close()


@manage_connection
def del_tool_request_by_userrequestid(user_request_id, connection=None):

    cursor = connection.cursor()
    cursor.execute('DELETE FROM tool_requests WHERE user_request_id = ?', (user_request_id,))

    connection.commit()
    connection.close()

if not os.path.exists(os.path.abspath(TEMP_DB_FOLDER)):
    print("path doesn't exist")
    os.makedirs(os.path.abspath(TEMP_DB_FOLDER))
if not is_database_present():
    create_database()