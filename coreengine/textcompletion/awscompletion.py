'''
LLM Completion using AWS Titan
'''
import os
import json
import logging
import yaml
import boto3
from coreengine.vault.azurevault import GenLiteAzureVault

logger=logging.getLogger("GenLiteApp")

class AWSTitanCompletion:
    '''LLM Completion using AWS Titan'''

    def __init__(self):
        '''
        Constructor
        '''
        self.configfilepath = 'coreengine/textcompletion/config.yaml'
        self.config = self.__loadconfig__(self.configfilepath)

        # Extract the configuration for the given template type
        template_config = self.config.get("awstitan", {})

        self.aws_access_key_id = template_config.get('aws_access_key_id', '')
        if self.aws_access_key_id == 'azurevault':

            aws_access_key_id_vault_key = template_config.get('aws_access_key_id_vault_key', '')
            if os.environ.get(aws_access_key_id_vault_key) is None:
                # Get the API key from the Azure Key Vault
                azure_vault = GenLiteAzureVault()
                self.aws_access_key_id = azure_vault.get_secret(aws_access_key_id_vault_key)
                os.environ[aws_access_key_id_vault_key] = self.aws_access_key_id
            else:
                self.aws_access_key_id = os.environ.get(aws_access_key_id_vault_key)

        self.aws_secret_access_key = template_config.get('aws_secret_access_key', '')
        if self.aws_secret_access_key == 'azurevault':

            aws_secret_access_key_vault_key = template_config.get(
                'aws_secret_access_key_vault_key',
                ''
                )
            if os.environ.get(aws_secret_access_key_vault_key) is None:
                # Get the API key from the Azure Key Vault
                azure_vault = GenLiteAzureVault()
                self.aws_secret_access_key = azure_vault.get_secret(aws_secret_access_key_vault_key)
                os.environ[aws_secret_access_key_vault_key] = self.aws_secret_access_key
            else:
                self.aws_secret_access_key = os.environ.get(aws_secret_access_key_vault_key)

        self.service_name = template_config.get('service_name', '')
        self.region_name = template_config.get('region_name', '')
        self.modelid = template_config.get('modelId', '')

        maxtokencount = template_config.get('maxTokenCount', 6144)
        #convert max_output_tokens to int
        self.maxtokencount = int(maxtokencount)
        temperature = template_config.get('temperature', 0)
        #convert temperature to float
        self.temperature = float(temperature)
        top_p = template_config.get('topP', 0.5)
        #convert top_p to float
        self.top_p = float(top_p)

    def __loadconfig__(self, configfilepath):
        '''
        Loads the config file
        '''
        with open(configfilepath, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config

    def generate(self, systemprompt):
        '''
        Generate a completion
        '''

        returnresponse = ""
        body = json.dumps({
            "inputText": systemprompt, 
            "textGenerationConfig":{  
                "maxTokenCount":self.maxtokencount,
                "stopSequences":[],
                "temperature":self.temperature,
                "topP":self.top_p
            }
        })

        try:
            completionmodel = boto3.client(
                service_name=self.service_name,
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key= self.aws_secret_access_key
                )
            response = completionmodel.invoke_model(
                    body=body,
                    modelId=self.modelid,
                    accept="application/json",
                    contentType="application/json"
                )
            response_body = json.loads(response.get('body').read())
            returnresponse = response_body.get('results')[0].get('outputText')
            returnresponse=returnresponse.replace("```json","")
            returnresponse=returnresponse.replace("```","")
        except Exception as e:
            logger.error("Error: %s", e)
        return returnresponse
