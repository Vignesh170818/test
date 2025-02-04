'''
Google Code Completion Wrapper
'''
import os
import logging
import vertexai
import yaml
from dotenv import load_dotenv
from vertexai.language_models import CodeGenerationModel

load_dotenv()

logger=logging.getLogger("GenLiteApp")

class GoogleBisonCompletion:
    '''LLM Wrapper for Google Bison Completion'''

    def __init__(self):
        self.configfilepath = 'coreengine/codecompletion/config.yaml'
        self.config = self.__loadconfig__(self.configfilepath)

        # Extract the configuration for the given template type
        template_config = self.config.get("bisonconfig", {})
        self.googleproject = template_config.get('googleproject', '')
        self.googleservicelocation = template_config.get('googleservicelocation', '')
        self.modelname = template_config.get('modelname', '')
        self.json_key = template_config.get('json_key', '')
        max_output_tokens = template_config.get('max_output_tokens', 6144)
        #convert max_output_tokens to int
        max_output_tokens = int(max_output_tokens)
        temperature = template_config.get('temperature', 0)
        #convert temperature to float
        temperature = float(temperature)
        top_p = template_config.get('top_p', 0.5)
        #convert top_p to float
        top_p = float(top_p)
        self.parameters = {
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
            "top_p": top_p
            }

    def __loadconfig__(self, configfilepath):
        '''
        Loads the config file
        '''
        with open(configfilepath, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config

    def generate(self, systemprompt):
        '''
        Generates text using the LLM
        '''
        returnresponse = None

        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.json_key
            vertexai.init(
                project=self.googleproject,
                location=self.googleservicelocation
                )

            completionmodel = CodeGenerationModel.from_pretrained(
                self.modelname
            )
            response = completionmodel.predict(
                systemprompt,
                **self.parameters
                )
            returnresponse = response.text

        except Exception as e:
            logger.error("Error: %s", e)

        return returnresponse
