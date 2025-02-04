import os
import logging
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential,DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Load the .env file
load_dotenv()

logger=logging.getLogger("GenLiteApp")

class GenLiteAzureVault:
    '''Azure Key Vault class'''
    def __init__(self):
        '''
        Initialize the Azure Key Vault class
        '''

        # Get the environment variables
        self.tenant_id = os.getenv("MICROSOFT_PROVIDER_TENANT_ID")
        self.client_id = os.getenv("MICROSOFT_PROVIDER_CLIENT_ID")
        self.client_secret = os.getenv("MICROSOFT_PROVIDER_AUTHENTICATION_SECRET")
        self.key_vault_name = os.getenv("AZURE_VAULT_NAME")
        self.key_vault_url = os.getenv("AZURE_VAULT_URL")
        self.user_managed_identity = os.getenv("USER_ASSIGNED_MANAGED_IDENTITY")
        self.identity_type = os.getenv("IDENTITY_TYPE")

    def get_secret(self, secret_name):
        '''
        Get a secret from Azure Key Vault
        :param secret_name: The name of the secret to retrieve
        :return: The value of the secret
        '''

        try:

            # Authenticate with Azure using the client secret
            if self.identity_type.lower()=="defaultazurecredential":
                credential=DefaultAzureCredential(managed_identity_client_id=self.user_managed_identity)
            else:
                credential = ClientSecretCredential(
                    tenant_id=self.tenant_id,
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
            

            # Create a SecretClient using the credential
            secret_client = SecretClient(vault_url=self.key_vault_url, credential=credential)
            # Retrieve the secret from Azure Key Vault
            retrieved_secret = secret_client.get_secret(secret_name)
            # Output the value of the retrieved secret
            return retrieved_secret.value
        except Exception as e:
            logger.error("Error: %s", e)
            return None
