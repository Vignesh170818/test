'''App Extension Specific Library for Industry'''
from wtforms import SelectField

class GenLiteAppExtension:
    '''App Extension Specific Library for Industry'''

    def __init__(self):
        self.industryfilepath = "genliteappext/industry.csv"

    def load_industry(self) -> SelectField:
        '''Load Industry

        This method is used to load the industry choices into the industryselectfield.
        It appends the industry choices to the choices list of the industryselectfield.

        Args:
            industryselectfield (Field): The field to which the industry choices will be appended.

        Returns:
            Field: The industryselectfield with the industry choices appended.
        '''

        #read a csv and assign the values to the industryselectfield
        with open(
            self.industryfilepath,
            'r',
            encoding="utf8",
            errors='ignore'
            ) as industryfile:

            choiceslist = [("dummy", "Select Industry")]

            for industry in industryfile:
                industrykey = industry.split(',')[0].replace('"', '')
                industryvalue = industry.split(',')[1].replace('"', '')
                choiceslist.append((industrykey, industryvalue))

        industryselectfield = SelectField(
            'Industry',
            choices=choiceslist,
            render_kw={
                'class': 'form-control',
                'placeholder': 'Select Industry',
                'required': True
            }
        )

        return industryselectfield
