import json
import requests
from jira import JIRA
from configparser import ConfigParser, ExtendedInterpolation
import os
import sys
import time
import yaml
from tool_integration.fieldTransformation import mapJIRADictionaryTemplate
# from keyvaults.keyvault_manager import keyvault_manager
from sqlite_handler import handler
import logging
from coreengine.vault.azurevault import GenLiteAzureVault

module_logger = logging.getLogger("tool_integration.jiralistener")

class CloudJIRA:
    def __init__(self):
        self.server_url: str = None
        self.username_id: str = None
        self.password_id: str = None
        self.project: str = None

        configfilepath = 'tool_integration/config.yaml'
        with open(configfilepath, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        module_logger.info("Config file loaded")
        # Extract the configuration for the given template type
        template_config = config.get("cloudjira", {})
        module_logger.info("Jira details loaded from config file")
        self.username_id = template_config.get('username_id', '')
        module_logger.info("Checking the username_id: %s",self.username_id)
        if self.username_id == 'azurevault':
            
            if os.environ.get('CloudJiraUserName') is None:
                # Get the JIRA key from the Azure Key Vault
                azure_vault = GenLiteAzureVault()
                self.username_id = azure_vault.get_secret('CloudJiraUserName')
                self.password_id = azure_vault.get_secret('CloudJiraPassword')
                os.environ['CloudJiraUserName'] = self.username_id
                os.environ['CloudJiraPassword'] = self.password_id
                module_logger.info(f"JIRA details retrieved form key vault. Username: {self.username_id} Password: {self.password_id}")
            else:
                self.username_id = os.environ.get('CloudJiraUserName')
                self.password_id = os.environ.get('CloudJiraPassword')
                module_logger.info(f"JIRA details retrieved form env. Username: {self.username_id} Password: {self.password_id}")
        
        self.server_url = template_config.get('server_url', '')
        self.project = template_config.get('project', '')

def get_cloud_jira(config):
    module_logger.info("Method 'get_cloud_jira()' started")
    cloud_jira = CloudJIRA()
    module_logger.info("Method 'get_cloud_jira()' ended")
    return cloud_jira

entityName_mapping = {
            "epic": "Epic",
            "feature": "Custom Feature ",
            "userstory": "Story",
            "task": "Task"
        }

def get_jira_instance(connection_object,retryCount=3,waitDuration=5):
    for _ in range(retryCount):
        try:
            module_logger.info("Method 'get_jira_instance()' started")
            if connection_object.server_url and connection_object.username_id and connection_object.password_id:
                jira = JIRA(server= connection_object.server_url, basic_auth=(connection_object.username_id, connection_object.password_id))
                module_logger.info("Method 'get_jira_instance()' ended: Jira instance is instantiated.")
                return jira
            else:
                raise Exception("Jira Connection details are incomplete. Kindly correct the configuration")
        except Exception as ex:
                time.sleep(waitDuration)
                module_logger.error(f"Method 'get_jira_instance()': An error occurred: {str(ex)}")
                raise ex

def format_tasks(task_data):
    task_output_data = ''
    for key, value in task_data.items():
        task_output_data += f'\n{key}'
        subtasks = value.split('Sub Task')
        for i, subtask in enumerate(subtasks[1:], start=1):
            formatted_subtask = f'\n\tSub Task {subtask.strip()}'
            task_output_data += formatted_subtask
        task_output_data += '\n'
    return task_output_data

def userstory_links(jira_instance,project,us_externalId,jira_data):
    module_logger.info("Method 'userstory_links()' started")
    jql_query = f'issuetype = "Task" and issue in linkedIssues("{us_externalId}", "relates to") and project = '+project+' ORDER BY created asc'
    associated_tasks = jira_instance.search_issues(jql_query)
    task_dict_details={}
    for task in associated_tasks:
        task_summary= task.fields.summary
        task_description= task.fields.description
        task_dict_details[task_summary] = task_description
    if task_dict_details:
        task_dict_details=format_tasks(task_dict_details)
        jira_data['Task'] = task_dict_details
    module_logger.info("Method 'userstory_links()' ended")
    return jira_data
    
def get_jira_issue(external_id,config_data,entitytype):
    module_logger.info("Method 'get_jira_issue()' started")
    try:
        connection_object = get_cloud_jira(config_data)
        jira_instance = get_jira_instance(connection_object)
        response=''
        response=jira_instance.issue(external_id)
        entitytype=entitytype.lower()
        tool_entitytype= entityName_mapping[entitytype]
        if response:
            response_project=response.fields.project.key
            if response_project==connection_object.project:
                response_entitytype=response.fields.issuetype.name
                if response_entitytype==tool_entitytype:
                    jira_data=mapJIRADictionaryTemplate(external_id,response,entitytype,'inbound')
                    if entitytype=='userstory':
                        jira_data=userstory_links(jira_instance,connection_object.project,external_id,jira_data)
                    module_logger.info("Method 'get_jira_issue()' ended")
                    return jira_data
                else:
                    module_logger.error("IssueType of External Id is not matching with the EntityType")
                    raise ValueError(f"Entered externalId is not a/an {entitytype}")
            else:
                module_logger.error(f"Project configured is not matching with {entitytype} {external_id}")
                raise ValueError(f"Project configured is not matching with {entitytype} externalId")
        else:
            module_logger.error(f"Method 'get_jira_issue()': Failed to fetch Jira issues. Status code: {response.status_code}")
            raise FileNotFoundError("Details not found")
    except Exception as ex:
        module_logger.error(f"Method 'get_jira_issue()': Failed {str(ex)}")
        if response=='':
            raise FileNotFoundError("Issue does not exists")
        raise ex

def create_jira_issue(issue_data,jira_instance,entity_name,request_id,tool_request_id):
    module_logger.info(f"Method 'create_jira_issue()' started. Request_Id: {request_id}")
    try:
        handler.update_tool_request(request_id,tool_request_id=tool_request_id,status='INPROGRESS',status_reason='',tool_response='')
        tool_response = jira_instance.create_issue(issue_data)
        if tool_response:
            external_id = tool_response.key
            handler.update_tool_request(request_id,tool_request_id=tool_request_id,status='COMPLETED',status_reason='',tool_response=f'Successfully created with ExternalID: {external_id}')
            module_logger.info(f"Method 'create_jira_issue()' successsfully ended. Request_Id: {request_id}")
            return external_id
    except Exception as ex:
        handler.update_tool_request(request_id,tool_request_id=tool_request_id,status='FAILED',status_reason=f'Exception: {str(ex)}',tool_response='An error has occurred')
        module_logger.error(f"Method 'create_jira_issue()': Failed to create issue: {str(ex)}.. Request_Id: {request_id}")
        raise ex
    

def create_jira_issueLink(issuelink_data, jira_instance,request_id):
    module_logger.info(f"Method 'create_jira_issueLink()' started. Request_Id: {request_id}")
    try:
        if jira_instance:
            outward_issue = jira_instance.issue(issuelink_data['outwardIssue']['key'])
            inward_issue = jira_instance.issue(issuelink_data['inwardIssue']['key'])
            jira_instance.create_issue_link(issuelink_data['type']['name'], inward_issue, outward_issue)
            module_logger.info(f"Method 'create_jira_issueLink()' ended. Created JIRA_Issue_Link. Request_Id: {request_id}")
        else:
            module_logger.error(f"Method 'create_jira_issueLink()': Cannot create Jira issue link without a valid connection. Request_Id: {request_id}")
    except Exception as ex:
        module_logger.error(f"Method 'create_jira_issueLink()': Failed to create Jira issue link: {str(ex)}. Request_Id: {request_id}")
        raise ex

def delete_tasks_jira(jira_instance,project,us_externalId,request_id):
    module_logger.info(f"Method 'delete_tasks_jira()' started. Request_Id: {request_id}")
    try:
        jql_query = f'issuetype = "Task" and issue in linkedIssues("{us_externalId}", "relates to") and project = '+project+''
        associated_tasks = jira_instance.search_issues(jql_query)
        response = ""
        for task in associated_tasks:
            issue = jira_instance.issue(task.key)
            response = issue.delete()
        module_logger.info(f"Method 'delete_tasks_jira()' successsfully ended. Request_Id: {request_id}")
        return response
    except Exception as ex:
        module_logger.error(f"Method 'delete_tasks_jira()': Failed to create issue: {str(ex)}.. Request_Id: {request_id}")
        raise ex

def update_jira_issue(jira_instance,issue_data,entity_name,request_id,tool_request_id,tool_external_id=""):
    module_logger.info(f"Method 'update_jira_issue()' started. Request_Id: {request_id}")
    try:
        handler.update_tool_request(request_id,tool_request_id=tool_request_id,status='INPROGRESS',status_reason='',tool_response='')
        issue = jira_instance.issue(tool_external_id)
        issue.update(issue_data)
        external_id = tool_external_id
        handler.update_tool_request(request_id,tool_request_id=tool_request_id,status='COMPLETED',status_reason='',tool_response=f'Successfully updated ExternalID: {external_id}')
        module_logger.info(f"Method 'update_jira_issue()' successsfully ended. Request_Id: {request_id}")
        return external_id
    except Exception as ex:
        handler.update_tool_request(request_id,tool_request_id=tool_request_id,status='FAILED',status_reason=f'Exception: {str(ex)}',tool_response='An error has occurred')
        module_logger.error(f"Method 'update_jira_issue()': Failed to update issue: {str(ex)}.. Request_Id: {request_id}")
        raise ex

def update_external_service_with_retry(jira_instance,project,request_id,issue_data,entityName,parent_externalId="",tool_externalId="",retryCount=3,waitDuration=5):
    module_logger.info(f"Method 'update_external_service_with_retry()' started. Request_Id: {request_id}")
    for _ in range(retryCount):
        try:
            external_id = ""
            if jira_instance:
                issue_data.update({
                "project": project,
                "issuetype": {
                    "name": entityName_mapping[entityName]
                 }
                })

                from uuid import uuid1
                tool_request_id = str(uuid1())
                handler.insert_tool_request(request_id,tool_request_id,'JIRA',issue_data,entityName,'')
                external_id = update_jira_issue(jira_instance,issue_data,entityName,request_id,tool_request_id,tool_externalId)
            else:
                module_logger.error(f"Method 'update_external_service_with_retry()': Jira Instance is not initiated. Request_Id: {request_id}")
            if external_id:
                    break
            
        except Exception as ex:
            module_logger.error(f"Method 'update_external_service_with_retry()': An error occurred: {str(ex)}")
            raise ex

        time.sleep(waitDuration)
    module_logger.info(f"Method 'update_external_service_with_retry()' ended. Request_Id: {request_id}")
    return external_id

def create_external_service_with_retry(jira_instance,project,request_id,issue_data,entityName,parent_externalId="",retryCount=3,waitDuration=5):
    module_logger.info(f"Method 'call_external_service_with_retry()' started. Request_Id: {request_id}")
    for _ in range(retryCount):
        try:
            external_id = ""
            if jira_instance:
                issue_data.update({
                "project": project,
                "issuetype": {
                    "name": entityName_mapping[entityName]
                 }
                })

                from uuid import uuid1
                tool_request_id = str(uuid1())
                handler.insert_tool_request(request_id,tool_request_id,'JIRA',issue_data,entityName,'')
                external_id = create_jira_issue(issue_data,jira_instance,entityName,request_id,tool_request_id)
            else:
                module_logger.error(f"Method 'call_external_service_with_retry()': Jira Instance is not initiated. Request_Id: {request_id}")
            if external_id:
                    break
            
        except Exception as ex:
            module_logger.error(f"Method 'call_external_service_with_retry()': An error occurred: {str(ex)}")
            raise ex

        time.sleep(waitDuration)
    
    if external_id and parent_externalId != "":
        issuelink_data={
        "type": {
            "name": "Relates"
        },
        "inwardIssue": {
            "key": parent_externalId
        },
        "outwardIssue": {
            "key": external_id
        }
        }
        create_jira_issueLink(issuelink_data,jira_instance,request_id)
    module_logger.info(f"Method 'call_external_service_with_retry()' ended. Request_Id: {request_id}")
    return external_id

def notifyCloudListener(jira_instance,project,request_id,data,entity_name,parent_id=""):
    module_logger.info(f"Method 'notifyCloudListener()' started. Request_Id: {request_id}")    
    data["Title"] = data["Title"][:255] if "Title" in data else ""
    data["Acceptance Criteria"] = data["Acceptance Criteria"][:255] if "Acceptance Criteria" in data else ""
    tool_request = mapJIRADictionaryTemplate(request_id,data,entity_name)
    if tool_request:
        data["ExternalId"] = data["ExternalId"] if "ExternalId" in data else ""
        externalId = ""
        if data["ExternalId"]:
            externalId = data["ExternalId"]
        else:
            searchTitle = data["Title"].replace('"', '\\"')
            jql_query = 'project = '+ project +' AND summary ~"'+ searchTitle + '"'
            if entity_name != 'epic':
                jql_query = jql_query + ' AND issue in linkedIssues("'+ parent_id +'", "relates to")'
            issues_filtered = jira_instance.search_issues(jql_query)
            if issues_filtered:
                exact_match_issues = [issue for issue in issues_filtered if issue.fields.summary == data['Title']]
                externalId = exact_match_issues[0].key if exact_match_issues else ""
        if externalId:
            tool_external_id = update_external_service_with_retry(jira_instance,project,request_id,tool_request,entity_name,parent_id,externalId)
            if entity_name == 'userstory':
                delete_tasks_jira(jira_instance,project,externalId,request_id)            
        else:
            tool_external_id = create_external_service_with_retry(jira_instance,project,request_id,tool_request,entity_name,parent_id)
    else:
        module_logger.error(f"Method 'notifyCloudListener()': tool_request is empty. Request_Id: {request_id}")    
    module_logger.info(f"Method 'notifyCloudListener()' ended. Request_Id: {request_id}")
    return tool_external_id

def RequestCloudListener(data,supported_tool_entities,request_id,config_data):
    module_logger.info(f"Method 'RequestCloudListener()' started. Request_Id: {request_id}")
    try:
        connection_object = get_cloud_jira(config_data)
        project = connection_object.project
        jira_instance = get_jira_instance(connection_object)
        #get data from file
        # file_path = 'tool_integration/jsonQueue.json'
        # with open(file_path, 'r') as file:
        #     data = json.load(file)
        #get data from file end
        for epic in data['Epics'] if 'Epics' in data else []:
            epic_external_id = ""
            if "epic" in supported_tool_entities.cloudjira_supported_entities: 
                epic_external_id = notifyCloudListener(jira_instance,project,request_id,epic,"epic")
            for feature in epic['Features']  if 'Features' in epic else []:
                feature_external_id = ""
                if "feature" in supported_tool_entities.cloudjira_supported_entities:
                    feature_external_id = notifyCloudListener(jira_instance,project,request_id,feature,"feature", epic_external_id)
                for userstory in feature['UserStories']  if 'UserStories' in feature else []:
                    userstory_external_id = ""
                    if "userstory" in supported_tool_entities.cloudjira_supported_entities:
                        userstory_external_id = notifyCloudListener(jira_instance,project, request_id,userstory,"userstory", feature_external_id)
                    for task in userstory['Tasks'] if 'Tasks' in userstory else []:
                        task_external_id = ""
                        if "task" in supported_tool_entities.cloudjira_supported_entities:
                            task_external_id = notifyCloudListener(jira_instance,project, request_id,task,"task", userstory_external_id)
        module_logger.info(f"Method 'RequestCloudListener()' ended. Request_Id: {request_id}")
    except Exception as ex:
        module_logger.error(f"An error occurred: {str(ex)}")
        raise ex