"""
Created on Wed Oct 18 18:51:25 IST 2023

@author: kammari.vara.prasad

"""
import os,time,sys,traceback
import subprocess
from datetime import date, datetime, timedelta
import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor ,BasePoolExecutor
import requests
import logging
import sys
sys.path.append(".")
sys.path.append("..")
from sqlite_handler.handler import *
from logger_utils.get_logger import get_logger

logger = get_logger(filename="apscheduler.log")
logger.info("logger started")

this_file_path = os.path.abspath(os.path.dirname(__file__))
conf_file = os.path.join(this_file_path, '../pythonconfig.ini')

executors = {
    'default': ThreadPoolExecutor(8),
    # This limits total number of jobs running simulataneously ,bcs for a job to run , it needs thread resource 
    #'processpool': ProcessPoolExecutor(4)
    ##ProcessPool , it helps us to utilize multiple CPU cores , under each process we will be having thread pool executor
}
job_defaults = {
    'coalesce': True, # setting this true, making our job to run only once if it has skipped multiple runs 
    'misfire_grace_time': 15*60, # graceful time , each job can be wait after its scheduled time 
    'max_instances': 5    # this limits the maximum number of instances we can run simulateneously for a single job

}


SCHEDULER = BackgroundScheduler(job_defaults=job_defaults,executors=executors)


def poller():
    """
    This polls the database user_requests table every x mins and if found any new requests ,
    it triggers task_runner job with corresponding task. 
    """
    # logger.info(f"""
    #     --------------------------------------------------------
    #     Poller STARTED at {str(datetime.utcnow())}
    #     ---------------------------------------------------------
    #                         """)
    try:
        new_requests = retrieve_new_user_requests()
        if len(new_requests)==0:
            #logger.info(f"found no requests in this run")
            return 
        logger.info(f"found  {len(new_requests)} requests in this run")
        #No of user_requests to be processed?
        for request in new_requests:
            #update the current request status as QUEUED
            update_user_request(request['request_id'],status="QUEUED")
            task_runner_id = 'Integration_' + request['request_id']
            job_id = SCHEDULER.add_job(integration_runner,name="Integration_RUNNER",
            id=task_runner_id, 
            max_instances=1,
            replace_existing=False,
            next_run_time=datetime.now() + timedelta(seconds=10),
            args = [request['request_id']]
            )
        #max_instances will make sure that there is always maximum of one
        # instance of this job running at any given time
        

    except Exception as e:
        logger.error(f"{str(e)} occured while polling")
        tb = traceback.format_exc().split("\n")
        logger.error(str(tb))

    # logger.info(f"""
    #     --------------------------------------------------------
    #     Poller ENDED at {str(datetime.utcnow())}
    #     ---------------------------------------------------------
    #                         """)
    return 


def integration_runner(request_id):
    """
       This function runs the Tool Inetgration taking request_id as command line argument
    """
    try:
        # logger.info(f"""
        #     --------------------------------------------------------
        #    integration_runner started STARTED at {str(datetime.utcnow())}
        #     ---------------------------------------------------------
        #                         """)
        program_path = "tool_integration" + os.sep + "integration.py"
        command = 'python ' + program_path
        command += f" -r {request_id} "
        logger.info(f"""
        --------------------------------------------------------
           Tool inetgration STARTED for {command}
        ---------------------------------------------------------
                            """)
        start_time = datetime.utcnow()
        out = subprocess.run(
                        command,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True,
                        env = os.environ.copy()
                        )
    
        verbose = ''
        if out.returncode == 0:
            logger.info(f"successfully ran tool_integration for {request_id}")
            verbose = out.stdout
        else:
            logger.error(f"error might have occured while running the tool_integration for the request {request_id}")
            verbose = out.stderr
            logger.info(verbose)
        end_time = datetime.utcnow()
        logger.info(f"Tool Integration ran  for {request_id} start_time:{start_time} end_time :{end_time}")
        ##update_user_request(request_id=request_id, status_reason="Tool Integration errored"+ str(out.stderr))
    
    
    
    except Exception as e:
        logger.error(f"{str(e)} occured while running the Tool Integration for request {request_id}")
        tb = traceback.format_exc().split("\n")
        logger.error(str(tb))

    # logger.info(f"""
    #     --------------------------------------------------------
    #     Tool Integration ENDED at {str(datetime.utcnow())}
    #     ---------------------------------------------------------
    #                         """)

def delete_user_requests_job():
    try:
        logger.info(f"""
--------------------------------------------------------
DELETE A DAY OLDER DB ENTRIES STARTED
---------------------------------------------------------
                     """)
        
        del_user_request()
        del_tool_request()
        
        logger.info(f"""
--------------------------------------------------------
DELETE A DAY OLDER DB ENTRIES ENDED
---------------------------------------------------------
                     """)
    except Exception as e:
        logger.error(f"{str(e)} occured while running the delete user request table")
        tb = traceback.format_exc().split("\n")
        logger.error(str(tb))

def get_time_stamp():
    current_time_stamp = datetime.now()
    datestamp = current_time_stamp.strftime("%d%b%Y")
    timestamp = current_time_stamp.strftime("%H%M")
    return datestamp+"_"+timestamp

def check_database_integrity():  
    check=True   
    try:
        conn = sqlite3.connect(os.path.join(TEMP_DB_FOLDER, 'data.db'), timeout=15)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()[0]
        conn.close()
        # Check the result
        if result == 'ok':
            pass
            # logger.info("Database integrity check passed. The database is not corrupted.")
        else:
            logger.error("Database integrity check failed. There may be corruption or other issues.")
            check=False
            # os.rename("data.db", f"data_bkp_{get_time_stamp}.db")
    except Exception as e:
        print(f"SQLite error: {e}")
        check=False
    if check==False:    
        logger.error("\ndb integrity Check Failed hence, creating new db\n")
        os.rename("data.db", f"data_bkp_{get_time_stamp}.db")
        create_database()


if __name__ == '__main__':
    logger.info(f"""
--------------------------------------------------------
SCHEDULAR MAIN STARTED
---------------------------------------------------------
                     """)
    SCHEDULER.add_job(poller,
                       'interval',
                      seconds = 60,
                    #   minutes=1,
                      # TO DO make it configurable
                      name="POLLER",
                      max_instances=1,
                      # replace_existing=True,
                       #id="POLLING_JOB"
                    )
    SCHEDULER.add_job(delete_user_requests_job,
                       'interval',
                      seconds = 86400,
                    #   minutes=1,
                      # TO DO make it configurable
                      name="Delete Job Runner",
                      max_instances=1,
                    )
    SCHEDULER.add_job(check_database_integrity,
                       'interval',
                      seconds = 600,
                    #   minutes=1,
                      # TO DO make it configurable
                      name="DB Integrity Checker",
                      max_instances=1,
                    )
    
    SCHEDULER.start()
    while True:
        time.sleep(10)