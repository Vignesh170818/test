'''LLMManager class for managing LLM models'''
import os
import logging
import yaml
from openai import AzureOpenAI, OpenAIError
from coreengine.vault.azurevault import GenLiteAzureVault

logger=logging.getLogger("GenLiteApp")

class AzureEmbedding:
    '''Class for Generating SDLC Artifacts'''

    def __loadconfig__(self, configfilepath):
        '''
        Loads the config file
        '''
        with open(configfilepath, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config

    def __init__(self):
        '''
        Constructor
        '''
        self.configfilepath = 'coreengine/embedding/config.yaml'
        self.config = self.__loadconfig__(self.configfilepath)

        # Extract the configuration for the given template type
        template_config = self.config.get("azureconfig", {})
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

    def get_embedding(self, texttoembed):
        '''Gets completion prompt from LLM model based on user query.

        Args:
            prompttemplate (str): The user query to generate a completion prompt for.

        Returns:
            str: The generated completion prompt.
        '''
        trycount = 0
        messageslist = [texttoembed]
        while trycount < 5:
            try:
                embeddingmodel = AzureOpenAI(
                    azure_endpoint=self.azure_endpoint,
                    api_key=self.api_key,
                    azure_deployment=self.azure_deployment,
                    api_version=self.api_version
                )
                embedding = embeddingmodel.embeddings.create(
                        input=messageslist,
                        model=self.modelname
                    )
                response = embedding.data[0].embedding
                return response
            except OpenAIError as exception:
                response = "Error: " + str(exception)
                logger.error("Error: %s", exception)
                trycount += 1

        return response
