'''
This file contains the GenLiteLLMModel class which is used to 
load the industry choices into the industryselectfield and 
to get the industry label for the given industry key.
'''
from wtforms import SelectField

class GenLiteLLMModel:
    '''GenLite LLM Model'''

    def __init__(self):
        self.filepath = "coreengine/util/llmmodels.csv"

    def get_llmmodels_selectfield(self) -> SelectField:
        '''Load LLM Models
        '''

        #read a csv and assign the values to the industryselectfield
        with open(
            self.filepath,
            'r',
            encoding="utf-8",
            errors='ignore'
            ) as modelsfile:

            choiceslist = [("dummy", "Select Model")]

            for llmmodel in modelsfile:
                modelkey = llmmodel.split(',')[0].replace('"', '')
                modelvalue = llmmodel.split(',')[1].replace('"', '')
                choiceslist.append((modelkey, modelvalue))

        llmmodelselectfield = SelectField(
            'LLM Model',
            choices=choiceslist,
            render_kw={
                'class': 'form-control',
                'placeholder': 'Select Industry',
                'required': True
            }
        )

        return llmmodelselectfield
