
import ast
import msal
import logging
import traceback
logger = logging.getLogger("GenLiteApp")
from coreengine.vault.azurevault import GenLiteAzureVault
from settings import app_json


auth_enabled = app_json["ADAuthEnabled"]
key_vault_enabled = app_json.get("KeyVaultEnabled",False)
msal_config = {
    "auth_enabled" : "false",
    "client_id": None,
    "client_secret":None,
    "authority": None,
    "redirect_uri": None,
    "scope": None,
    "base_uri": None,
    "tenant_id": None
}
msal_client = None


if auth_enabled.lower().strip()=="true" and key_vault_enabled.lower().strip()=="true":
    azure_vault = GenLiteAzureVault()
    tenant_id = azure_vault.get_secret('TenantId')
    cloud_jira_user_name = azure_vault.get_secret('CloudJiraUserName')
    cloud_jira_password =  azure_vault.get_secret('CloudJiraPassword')
    msal_config = {
        "auth_enabled" : auth_enabled,
        "client_id": azure_vault.get_secret("ClientId"),
        "client_secret": azure_vault.get_secret("ClientSecret"),
        "authority": f"https://login.microsoftonline.com/{tenant_id}",
        "redirect_uri":  app_json["ADAuthConfig"]["BaseUri"].strip("/")+ app_json["ADAuthConfig"]["RedirectUri"],
        "scope": ["User.Read"],
        "error": False,
        "base_uri": app_json["ADAuthConfig"]["BaseUri"],
        "tenant_id": azure_vault.get_secret("TenantId"),
        "cloud_username" : cloud_jira_user_name,
        "cloud_password" : cloud_jira_password
    }
elif auth_enabled.lower().strip()=="true" and key_vault_enabled.lower().strip()=="false":
    msal_config = {
        "auth_enabled" : auth_enabled,
        "client_id": app_json["ADAuthConfig"]["ClientId"],
        "client_secret": app_json["ADAuthConfig"]["ClientSecret"],
        "authority": f"https://login.microsoftonline.com/{app_json['ADAuthConfig']['TenantId']}",
        "redirect_uri": app_json["ADAuthConfig"]["BaseUri"].strip("/")+ app_json["ADAuthConfig"]["RedirectUri"],
        "scope": ast.literal_eval(app_json["ADAuthConfig"]["Scope"]),
        "error": False,
        "base_uri": app_json["ADAuthConfig"]["BaseUri"],
        "tenant_id": app_json["ADAuthConfig"]["TenantId"]
    }

    
#MSAL Client
msal_client = None 
msal_client = msal.ConfidentialClientApplication(
        client_id= msal_config['client_id'],
        authority= msal_config['authority'],
        client_credential=msal_config['client_secret']
    )

    