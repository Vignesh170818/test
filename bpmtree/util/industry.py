'''App Extension Specific Library for Industry'''

class GenLiteIndustry:
    '''App Extension Specific Library for Industry'''

    def __init__(self):
        self.industryfilepath = "bpmtree/util/industry.csv"

    def get_industry_choices(self) -> list:
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
            encoding="utf-8",
            errors='ignore'
            ) as industryfile:

            choiceslist = [("dummy", "Select Industry")]

            for industry in industryfile:
                industrykey = industry.split(',')[0].replace('"', '')
                industryvalue = industry.split(',')[1].replace('"', '')
                choiceslist.append((industrykey, industryvalue))

        return choiceslist

    def get_industry_label(self, industrykey: str) -> str:
        '''Get Industry Label

        This method is used to get the industry label for the given industry key.

        Args:
            industrykey (str): The industry key for which the industry label is to be fetched.

        Returns:
            str: The industry label for the given industry key.
        '''
        industrylabel = ""
        with open(
            self.industryfilepath,
            'r',
            encoding="utf-8",
            errors='ignore'
            ) as industryfile:

            for industry in industryfile:
                if industry.split(',')[0].replace('"', '') == industrykey:
                    industrylabel = industry.split(',')[1].replace('"', '')
                    break

        return industrylabel
