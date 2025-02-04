'''Functional Design generative model for image recognition using Google Vision API'''
import os
import logging
import vertexai
import yaml
from vertexai.preview.generative_models import GenerativeModel, Image

logger=logging.getLogger("GenLiteApp")

class GoogleVisionCompletionModel:
    '''Class for Generating SDLC Artifacts using Google Vision API.'''

    def __loadconfig__(self, configfilepath):
        '''
        Loads the config file
        '''
        with open(configfilepath, 'r', encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config

    def __init__(self):
        '''
        Constructor
        '''
        self.configfilepath = 'coreengine/multimodal/config.yaml'
        self.config = self.__loadconfig__(self.configfilepath)

        # Extract the configuration for the given template type
        template_config = self.config.get("geminiconfig", {})
        self.googleproject = template_config.get('googleproject', '')
        self.googleservicelocation = template_config.get('googleservicelocation', '')
        self.modelname = template_config.get('modelname', '')
        self.json_key = template_config.get('json_key', '')

    def generate(self, image_path, systemprompt):
        '''Get the functional design from the given image path using Google Vision API.'''

        json_key = self.json_key
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_key
        vertexai.init(
            project=self.googleproject,
            location=self.googleservicelocation
            )
        image = Image.load_from_file(image_path)
        generative_multimodal_model = GenerativeModel(
            self.modelname
            )
        response = generative_multimodal_model.generate_content([systemprompt, image])
        logger.info(
            response.candidates[0].content.text
            )
        return response.candidates[0].content.text
