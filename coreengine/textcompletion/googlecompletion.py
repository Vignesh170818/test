'''Text Generation using Google LLM'''
import os
import logging
import vertexai
import yaml
from dotenv import load_dotenv
from vertexai.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.generative_models import HarmCategory, HarmBlockThreshold

load_dotenv()

logger=logging.getLogger("GenLiteApp")

class GoogleBisonCompletion:
    '''LLM Wrapper for Google Bison Completion'''

    def __init__(self):
        self.configfilepath = 'coreengine/textcompletion/config.yaml'
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
        with open(configfilepath, 'r', encoding="utf-8") as file:
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

            completionmodel = TextGenerationModel.from_pretrained(
                self.modelname
            )
            response = completionmodel.predict(
                systemprompt,
                **self.parameters
                )
            returnresponse = response.text

        except Exception as e:
            logger.error(f"Error while generating text using the LLM. Error: ({e})")

        return returnresponse

class GoogleGeminiCompletion:
    '''LLM Wrapper for Google Gemini Completion'''

    def __init__(self):
        '''
        Constructor
        '''
        self.configfilepath = 'coreengine/textcompletion/config.yaml'
        self.config = self.load_config(self.configfilepath)

        # Extract the configuration for the given template type
        template_config = self.config.get("geminiconfig", {})
        self.googleproject = template_config.get('googleproject', '')
        self.googleservicelocation = template_config.get('googleservicelocation', '')
        self.modelname = template_config.get('modelname', '')
        self.json_key = template_config.get('json_key', '')
        max_output_tokens = template_config.get('max_output_tokens', 6144)
        temperature = template_config.get('temperature', 0)
        top_p = template_config.get('top_p', 0.5)
        self.geminiconfig = {
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
            "top_p": top_p
            }

    def load_config(self, configfilepath):
        '''
        Loads the config file
        '''
        with open(configfilepath, 'r', encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config

    def generate(self, systemprompt):
        '''
        Generates a response from the LLM model
        '''
        returnresponse = None

        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.json_key
            vertexai.init(
                project=self.googleproject,
                location=self.googleservicelocation
                )
            model = GenerativeModel(
                self.modelname
                )
            responses = model.generate_content(
                systemprompt,
                generation_config={
                    "max_output_tokens": 2048,
                    "temperature": 0.9,
                    "top_p": 1
                },
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                },
                stream=False,
            )
            returnresponse = responses.text
        except Exception as e:
            logger.error(f"Error: ({e})")
            returnresponse = None
        return returnresponse
