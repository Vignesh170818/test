import json
import sys
sys.path.append('.')
from tool_integration import jiralistener,almlistener,tool_settings
from sqlite_handler import handler
import os
import logging
import traceback

logger = logging.getLogger("tool_integration")
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler("/home/LogFiles/tool_integration.log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

logger.info("Starting GenLite App")

class ToolEntity:
    def __init__(self):
        self.cloudjira_supported_entities = []
        self.hpalm_supported_entities = []

def get_tool_entity(config):
    logger.info(f"Method 'get_tool_entity()' started")
    tool_entity = ToolEntity()
    sec = 'tool_entity'
    tool_entity.cloudjira_supported_entities = config[sec]["cloudjira"]
    tool_entity.hpalm_supported_entities = config[sec]["hpalm"]
    logger.info(f"Method 'get_tool_entity()' ended")
    return tool_entity

cp = tool_settings.get_config_path()

def read_data_from_service(request_id):
    logger.info(f"Method 'read_data_from_service()' started. Request_Id: {request_id}")
    try:
        if request_id:
            user_req = handler.retrieve_user_request(request_id)
            handler.update_user_request(request_id=request_id,status='INPROGRESS',status_reason='')
            supported_tools = get_tool_entity(cp)
            if (user_req["file_content"] and supported_tools):
                data = json.loads(user_req["file_content"]) 
            if (data and supported_tools):
                #Implementation for Cloud
                if any(key in data for key in ["Epics","Features","UserStories","Tasks"]):
                    status_reason = jiralistener.RequestCloudListener(data,supported_tools,request_id,cp)
                #Implementation for HPALM
                if any(key in data for key in ['Tests']):
                    status_reason = almlistener.RequestALMListener(data,supported_tools,request_id,cp)
                handler.update_user_request(request_id=request_id, status="COMPLETED", status_reason='')                
            else:
                handler.update_user_request(request_id=request_id,status='FAILED',status_reason='Invalid Data')
        else:
            handler.update_user_request(request_id=request_id,status='FAILED',status_reason='Request Id is empty')
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        tb = traceback.format_exc().split("\n")
        logger.error(f"traceback: {str(tb)}")
        handler.update_user_request(request_id=request_id, status="FAILED", status_reason=f"Exception: {str(e)} + {str(tb)}")

    logger.info(f"Method 'read_data_from_service()' ended. Request_Id: {request_id}")

def parse_data(data,entity_type):
    formatted_output=''
    logger.info(f"Method 'parse_data()'started")
    if entity_type=='epic':
         entity_type=entity_type.upper()
    elif entity_type=='userstory':
         entity_type='User Story'
    else:
        entity_type=entity_type.capitalize()
    if data:
        title = data.get('Title', None)
        selected_entity = title.replace(',', ',\n').replace('.', '.\n')
        if entity_type=='Feature':
            selected_entity= "{} 1:{}\n".format(entity_type,selected_entity)
            feature_Description = data.get('Description', '')
            selected_entity+= " -Description: {}\n\n".format(feature_Description)
        elif entity_type=='User Story':
            selected_entity= "{} 1:\n{}".format(entity_type,selected_entity)
        else:
            selected_entity= "{} :{}".format(entity_type,selected_entity)

        fields_dict = {
            'EPIC': ["Title", "Acceptance Criteria"],
            'Feature': ["Title"],
            'User Story': ["Acceptance Criteria", "Task"]
            }
        entity_fields = fields_dict.get(entity_type, [])
        formatted_output = ""

        if entity_fields:
            counter = 0
            for field in entity_fields:   
                field_value = data.get(field, '')
                counter += 1
                if field == 'Title' and entity_type != 'User Story':
                    title_field = f"{entity_type} {field}"
                    formatted_output += "{}. {}:{}\n\n".format(counter, title_field, field_value)    
                elif field =='Task':
                     formatted_output+= "{}".format(field_value)
                else:
                     formatted_output += "{}. {}:\n{}\n\n".format(counter,field,field_value if field_value != None else '' )
        logger.info(f"Method 'parse_data()' ended")
        return selected_entity,formatted_output
    else:
        logger.error(f"Method 'parse_data()': Errored")

def get_entityData(externalid,entitytype):
    logger.info(f"Method 'get_entityData()' started")
    supported_tools = get_tool_entity(cp)
    try:
        if (entitytype.lower() in supported_tools.cloudjira_supported_entities):
            data_object=jiralistener.get_jira_issue(externalid,cp,entitytype)
        elif (entitytype.lower() in supported_tools.hpalm_supported_entities):
            data_object= almlistener.get_alm_issue(externalid,cp)
        else:
            raise ValueError("Unsupported entity type")
    except Exception as ex:
        logger.error(f"Method 'get_entityData()': Failed {str(ex)}")
        raise ex

    selected_entity,entity_abstract=parse_data(data_object,entitytype)
    logger.info(f"Method 'get_entityData()' ended")
    return selected_entity,entity_abstract
                    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="A Python script with command-line arguments")
    parser.add_argument("--request_id",'-r', default="request_id", help="Description of request_id")
    args = parser.parse_args()
    request_id = args.request_id.strip()
    read_data_from_service(request_id)
