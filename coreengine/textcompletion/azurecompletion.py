'''LLM Completion Model for Azure OpenAI GPT 3.5 and GPT 4'''
import os
import logging
import yaml
import time
from openai import AzureOpenAI, OpenAIError, AsyncAzureOpenAI
from coreengine.vault.azurevault import GenLiteAzureVault

logger=logging.getLogger("GenLiteApp")

class AzureGPT35Completion:
    '''
    AzureGPT35Completion
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.configfilepath = 'coreengine/textcompletion/config.yaml'
        self.config = self.__loadconfig__(self.configfilepath)

        # Extract the configuration for the given template type
        template_config = self.config.get("azuregpt35config", {})
        self.api_key = template_config.get('api_key', '')
        if self.api_key == 'azurevault':

            api_key_vault_key = template_config.get('api_key_vault_key', '')
            if os.environ.get(api_key_vault_key) is None:
                # Get the API key from the Azure Key Vault
                azure_vault = GenLiteAzureVault()
                self.api_key = azure_vault.get_secret(api_key_vault_key)
                os.environ[api_key_vault_key] = self.api_key
            else:
                self.api_key = os.environ.get(api_key_vault_key)

        self.azure_endpoint = template_config.get('azure_endpoint', '')
        self.api_version = template_config.get('api_version', '')
        self.azure_deployment = template_config.get('azure_deployment', '')
        self.modelname = template_config.get('modelname', '')

        max_output_tokens = template_config.get('max_output_tokens', 6144)
        #convert max_output_tokens to int
        self.max_output_tokens = int(max_output_tokens)
        temperature = template_config.get('temperature', 0)
        #convert temperature to float
        self.temperature = float(temperature)
        top_p = template_config.get('top_p', 0.5)
        #convert top_p to float
        self.top_p = float(top_p)

    def __loadconfig__(self, configfilepath):
        '''
        Loads the config file
        '''
        with open(configfilepath, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config

    async def generate_async(self, systemprompt):
        '''
        Generate a completion
        '''

        returnresponse = ""
        messageslist = [
            {
                "role": "system",
                "content": systemprompt
            }
        ]
        try:
            completionmodel = AsyncAzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            azure_deployment=self.azure_deployment,
            api_version=self.api_version
            )
            azurecompletion = await completionmodel.chat.completions.create(
                    model=self.modelname,
                    messages=messageslist,
                    temperature=self.temperature,
                    top_p=self.top_p
                )
            returnresponse = azurecompletion.choices[0].message.content
        except OpenAIError as exception:
            logger.error("Error: %s", exception)
            returnresponse = "Error: " + str(exception)

        return returnresponse
    
    def generate(self, systemprompt):
        '''
        Generate a completion
        '''

        returnresponse = ""
        messageslist = [
            {
                "role": "system",
                "content": systemprompt
            }
        ]
        try:
            completionmodel = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            azure_deployment=self.azure_deployment,
            api_version=self.api_version
            )
            azurecompletion = completionmodel.chat.completions.create(
                    model=self.modelname,
                    messages=messageslist,
                    temperature=self.temperature,
                    top_p=self.top_p
                )
            returnresponse = azurecompletion.choices[0].message.content
        except OpenAIError as exception:
            logger.error("Error: %s", exception)
            returnresponse = "Error: " + str(exception)

        return returnresponse
    
    def generateStream(self, systemprompt):
        '''
        Generate a completion
        '''
        
        messageslist = [
            {
                "role": "system",
                "content": systemprompt
            }
        ]
        try:
            completionmodel = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            azure_deployment=self.azure_deployment,
            api_version=self.api_version
            )
            azurecompletion = completionmodel.chat.completions.create(
                    model=self.modelname,
                    messages=messageslist,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    stream=True
                )
            
            for chunk in azurecompletion:
                 if len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        time.sleep(0.05)
                        yield(delta.content)
                        
        except OpenAIError as exception:
            logger.error("Error: %s", exception)
            yield "Error: " + str(exception)

class AzureGPT4Completion:
    '''
    AzureGPT4Completion
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.configfilepath = 'coreengine/textcompletion/config.yaml'
        self.config = self.__loadconfig__(self.configfilepath)

        # Extract the configuration for the given template type
        template_config = self.config.get("azuregpt4config", {})
        self.api_key = template_config.get('api_key', '')
        if self.api_key == 'azurevault':

            api_key_vault_key = template_config.get('api_key_vault_key', '')
            if os.environ.get(api_key_vault_key) is None:
                # Get the API key from the Azure Key Vault
                azure_vault = GenLiteAzureVault()
                self.api_key = azure_vault.get_secret(api_key_vault_key)
                os.environ[api_key_vault_key] = self.api_key
            else:
                self.api_key = os.environ.get(api_key_vault_key)

        self.azure_endpoint = template_config.get('azure_endpoint', '')
        self.api_version = template_config.get('api_version', '')
        self.azure_deployment = template_config.get('azure_deployment', '')
        self.modelname = template_config.get('modelname', '')

        max_output_tokens = template_config.get('max_output_tokens', 6144)
        #convert max_output_tokens to int
        self.max_output_tokens = int(max_output_tokens)
        temperature = template_config.get('temperature', 0)
        #convert temperature to float
        self.temperature = float(temperature)
        top_p = template_config.get('top_p', 0.5)
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
        messageslist = [
            {
                "role": "system",
                "content": systemprompt
            }
        ]
        try:
            completionmodel = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            azure_deployment=self.azure_deployment,
            api_version=self.api_version
            )
            azurecompletion = completionmodel.chat.completions.create(
                    model=self.modelname,
                    messages=messageslist,
                    temperature=self.temperature,
                    top_p=self.top_p
                )
            returnresponse = azurecompletion.choices[0].message.content
        except OpenAIError as exception:
            logger.error("Error: %s", exception)
            returnresponse = "Error: " + str(exception)

        return returnresponse

    async def generate_async(self, systemprompt):
        '''
        Generate a completion
        '''

        returnresponse = ""
        messageslist = [
            {
                "role": "system",
                "content": systemprompt
            }
        ]
        try:
            completionmodel = AsyncAzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            azure_deployment=self.azure_deployment,
            api_version=self.api_version
            )
            azurecompletion = await completionmodel.chat.completions.create(
                    model=self.modelname,
                    messages=messageslist,
                    temperature=self.temperature,
                    top_p=self.top_p
                )
            returnresponse = azurecompletion.choices[0].message.content
        except OpenAIError as exception:
            logger.error("Error: %s", exception)
            returnresponse = "Error: " + str(exception)

        return returnresponse
