import time
import json
import os
import yaml
import requests
import logging
from sqlite_handler import handler
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
# from keyvaults.keyvault_manager import keyvault_manager
from tool_integration.fieldTransformation import mapHPALMDictionaryTemplate
from coreengine.vault.azurevault import GenLiteAzureVault

module_logger = logging.getLogger("tool_integration.almlistener")

class HPALM:
    def __init__(self):
        self.username_id: str = None
        self.password_id: str = None
        
        configfilepath = 'tool_integration/config.yaml'
        with open(configfilepath, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        # Extract the configuration for the given template type
        template_config = config.get("hpalm", {})
        self.username_id = template_config.get('username_id', '')
        if self.username_id == 'azurevault':
            HpalmUserName = template_config.get('HpalmUserName', '')
            if os.environ.get(HpalmUserName) is None:
                # Get the HPALM key from the Azure Key Vault
                azure_vault = GenLiteAzureVault()
                self.username_id = azure_vault.get_secret(HpalmUserName)
                os.environ[HpalmUserName] = self.username_id
                module_logger.info("HPALM Username retrieved form key vault: ", self.username_id)
            else:
                self.username_id = os.environ.get(HpalmUserName)

        self.password_id = template_config.get('password_id', '')
        if self.password_id == 'azurevault':
            HpalmPassword = template_config.get('HpalmPassword','')
            if os.environ.get(HpalmPassword) is None:
                # Get the HPALM key from the Azure Key Vault
                azure_vault = GenLiteAzureVault()
                self.password_id = azure_vault.get_secret(HpalmPassword)
                os.environ[HpalmPassword] = self.password_id
                module_logger.info("HPALM Password retrieved form key vault: ", self.password_id)
            else:
                self.password_id = os.environ.get(HpalmPassword)
        
        
        self.baseUrl = template_config.get('baseUrl', '')
        self.domain = template_config.get('domain', '')
        self.project = template_config.get('project', '')
        self.cookies = {}
        self.headers = {
            'cache-control': "no-cache",
            'Accept': "application/json",
            'Content-Type': "application/json"
        }

def get_hpalm(config):
        module_logger.info("Method 'get_hpalm()' started")
        hpalm = HPALM()
        module_logger.info("Method 'get_hpalm()' ended")
        return hpalm

entityName_mapping = {
            "test": "Test"
        }

def hpalm_logout(alm_instance):
        try:
            #delete cookie
            qccookieEndPoint = alm_instance.baseUrl + "rest/site-session"
            cookie_response = requests.delete(qccookieEndPoint, headers=alm_instance.headers, cookies=alm_instance.cookies)
            if(cookie_response.status_code == 200 or cookie_response.status_code == 201):
                alm_instance.cookies = {}
                alm_instance.headers = {}
                module_logger.info("Header and Cookies are deleted Successfully from HPALM")
            #sign out
            signout_EndPoint = alm_instance.baseUrl + "api/authentication/sign-out"
            signout_response = requests.get(signout_EndPoint, headers=alm_instance.headers)
            if(signout_response.status_code == 200 or signout_response.status_code == 201):
                module_logger.info("Sign out Successfully from HPALM")
            #logout
            qcLogoutEndPoint = alm_instance.baseUrl + "authentication-point/logout"
            logout_response = requests.get(qcLogoutEndPoint, headers=alm_instance.headers)
            if(logout_response.status_code == 200 or logout_response.status_code == 201):
                module_logger.info("Logged out Successfully from HPALM")
        except Exception as ex:
            module_logger.error(f"Error while logging out. Error: ({ex})")
            raise ex
        return

def get_alm_instance(connection_object,retryCount=3,waitDuration=5):
        module_logger.info("Method 'get_alm_instance()' started")
        try:
            for _ in range(retryCount):
                authEndPoint = connection_object.baseUrl + "api/authentication/sign-in"
                response = requests.post(authEndPoint, auth=HTTPBasicAuth(connection_object.username_id, connection_object.password_id), headers=connection_object.headers)
                if response.status_code == 200:
                    cookies = response.cookies
                    lwsso_cookie = response.cookies.get('LWSSO_COOKIE_KEY')
                    qcsession = response.cookies.get('QCSession')                    
                    xsrf_token = response.cookies.get('XSRF-TOKEN')                    
                    connection_object.cookies['LWSSO_COOKIE_KEY'] = lwsso_cookie
                    connection_object.cookies['QCSession'] = qcsession
                    connection_object.cookies['XSRF-TOKEN'] = xsrf_token
                    connection_object.headers['X-XSRF-TOKEN'] = xsrf_token
                    module_logger.info("Method 'get_alm_instance()' : Cookie generated successfully")                                                     
                    return connection_object
                else:
                    if _ < retryCount - 1:
                        time.sleep(waitDuration)
                    else:
                        raise Exception(f"Error while connecting to hpalm instance. Status code: {response.status_code} Reason: {response.reason}")
        except Exception as ex:
            module_logger.error(f"Method 'get_alm_instance()' : HPALM instance cannot be instantiated. {str(ex)}")
            raise ex

def create_alm_issue(issue_data,alm_instance,serviceUrl,request_id,tool_request_id):
    module_logger.info(f"Method 'create_alm_issue()' started. Request_Id: {request_id}")
    try:
        handler.update_tool_request(request_id,tool_request_id=tool_request_id,status='INPROGRESS',status_reason='',tool_response='')
        response = requests.post(serviceUrl, headers=alm_instance.headers, json= issue_data, cookies=alm_instance.cookies)
        if(response.status_code==201):
            data = json.loads(response.text)
            for field in data["Fields"]:
                if field["Name"] == "id":
                    external_id = field["values"][0]["value"]
                    handler.update_tool_request(request_id,tool_request_id=tool_request_id,status='COMPLETED',status_reason='',tool_response=f'Successfully created with ExternalID: {external_id}')
                    module_logger.info(f"Method 'create_alm_issue()' ended. Request_Id: {request_id}")
                    return external_id
        else:
            module_logger.error(f"Failed to create the issue with reason as '{response.reason}' - '{response.text}' and status as '{response.status_code}'")
            raise Exception(f"Failed to create the issue with reason as '{response.reason}' - '{response.text}' and status as '{response.status_code}'")
    except Exception as ex:
        module_logger.error(f"Method 'create_alm_issue()': Failed to create issue: {str(ex)}.{response.reason}. Request_Id: {request_id}")
        handler.update_tool_request(request_id,tool_request_id=tool_request_id,status='FAILED',status_reason=f'Exception: {str(ex)} {response.reason}',tool_response='An error has occurred')
        raise ex

def get_alm_issue(externalid,config_data) -> None:
        connection_object = get_hpalm(config_data)
        alm_instance = get_alm_instance(connection_object)
        try: 
            testUrl = alm_instance.baseUrl + "rest/domains/" + alm_instance.domain + "/projects/" + alm_instance.project + "/tests/" +externalid
            response = requests.get(testUrl, cookies=alm_instance.cookies)
            if(response.status_code==200):
                root = ET.fromstring(response.text)
                externalid = root.find(".//Field[@Name='id']")
                summary = root.find(".//Field[@Name='name']")
                description = root.find(".//Field[@Name='description']")
                hpalm_data = {
                'external_id' : externalid.find('Value').text if externalid is not None and externalid.find('Value') is not None else None,
                    'summary':summary.find('Value').text if summary is not None and summary.find('Value') is not None else None,
                    'description':description.find('Value').text if description is not None and description.find('Value') is not None else None
                }
        except Exception as ex: 
            module_logger.error(f"Hpalm error ({ex})")
        return hpalm_data

def call_external_service_with_retry(request_id,alm_instance,issue_data,entityName,parent_externalId="",retryCount=3,waitDuration=5):
    module_logger.info(f"Method 'call_external_service_with_retry()' started. Request_Id: {request_id}")
    for _ in range(retryCount):
        try:
            external_id = ""
            if alm_instance:
                serviceUrl = ""
                if entityName == 'test':
                    serviceUrl = alm_instance.baseUrl + "rest/domains/" + alm_instance.domain + "/projects/" + alm_instance.project + "/tests"
                elif entityName == 'teststep':
                    serviceUrl = alm_instance.baseUrl + "rest/domains/" + alm_instance.domain + "/projects/" + alm_instance.project + "/design-steps?query={parent-id[" + parent_externalId + "]}"
                from uuid import uuid1
                tool_request_id = str(uuid1())
                handler.insert_tool_request(request_id,tool_request_id,'HPALM',issue_data,entityName,'')
                external_id = create_alm_issue(issue_data,alm_instance,serviceUrl,request_id,tool_request_id)
            else:
                module_logger.error(f"Method 'call_external_service_with_retry()': ALM Instance is not initiated. Request_Id: {request_id}")
            if external_id:
                    break
        except Exception as ex:
            module_logger.error(f"Method 'call_external_service_with_retry()': An error occurred: {str(ex)}")
            raise ex
        time.sleep(waitDuration)
    module_logger.info(f"Method 'call_external_service_with_retry()' ended. Request_Id: {request_id}")
    return external_id

def notifyALMListener(request_id,alm_instance,data,entity_name,parent_id=""):
    module_logger.info(f"Method 'notifyALMListener()' started. Request_Id: {request_id}")
    data["Title"] = data["Title"][:255] if "Title" in data else ""
    tool_request = mapHPALMDictionaryTemplate(request_id,data,entity_name,parent_id)
    if tool_request:
        tool_external_id = call_external_service_with_retry(request_id,alm_instance,tool_request,entity_name,parent_id)
    else:
        module_logger.error(f"Method 'notifyALMListener()': tool_request is empty. Request_Id: {request_id}")    
    module_logger.info(f"Method 'notifyALMListener()' ended. Request_Id{request_id}") 
    return tool_external_id

def checkInOutEntity(alm_instance,state,parent_external_id):
    parent_external_id=str(parent_external_id)
    url=""
    checkOutOrInEndPoint=""
    url= alm_instance.baseUrl + "rest/domains/" + alm_instance.domain + "/projects/" + alm_instance.project + "/tests/" + parent_external_id + "/versions/"
    if state=='checkout':
        checkOutOrInEndPoint= url + 'check-out?login-form-required=y'
    else:
        checkOutOrInEndPoint= url + 'check-in?login-form-required=y'
    if checkOutOrInEndPoint and alm_instance:
        response = requests.post(checkOutOrInEndPoint, headers=alm_instance.headers, json= {}, cookies=alm_instance.cookies)
        if(response.status_code == 200 or response.status_code == 201):
            module_logger.info(f"Method 'check()' : checkOutOrInEndPoint : {state} successful")
    return

def RequestALMListener(data,supported_tool_entities,request_id,cp):
    module_logger.info(f"Method 'RequestALMListener()' started. Request_Id: {request_id}")
    try:
        global config_data
        config_data = cp
        connection_object = get_hpalm(config_data)
        alm_instance = get_alm_instance(connection_object)
        for test in data['Tests'] if 'Tests' in data else []:
            test_external_id= ""
            if "test" in supported_tool_entities.hpalm_supported_entities:
                test_external_id = notifyALMListener(request_id,alm_instance,test,"test")
                if 'TestSteps' in test and test_external_id:
                    checkInOutEntity(alm_instance,'checkout',test_external_id)
                    for testStep in test['TestSteps']  if 'TestSteps' in test else []:
                        teststep_external_id = ""
                        teststep_external_id = notifyALMListener(request_id,alm_instance,testStep,"teststep",test_external_id)
                    checkInOutEntity(alm_instance,'checkin',test_external_id)
        hpalm_logout(alm_instance)
        module_logger.info(f"Method 'RequestALMListener()' ended. Request_Id: {request_id}")
    except Exception as ex:
        module_logger.error(f"An error occurred: {str(ex)}")
        hpalm_logout(alm_instance)
        raise ex