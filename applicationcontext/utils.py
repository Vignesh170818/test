'''
This module contains utility functions for the GenLite project.
'''
import json
import logging
import regex as re

logger=logging.getLogger("GenLiteApp")

def json_to_stringbpm(jsontext, replaceline="<br>"):
    '''Get incident category from json'''

    corrected_str = re.sub(r',(\s*[}\]])', r'\1', jsontext)
    try:
        jsonbpm = json.loads(corrected_str)
        stringbpm = ""
        for _, value in jsonbpm.items():
            for key1, value1 in value.items():
                stringbpm += f"{key1}: {value1}"
                stringbpm += replaceline
        incidentcategory = stringbpm
        return incidentcategory
    except json.JSONDecodeError as e:
        logger.error("JSON Decode Error: %s", e)
        logger.debug("JSON Text: %s", jsontext)
        return jsontext

def get_application_context(industry: str) -> str:
    '''Returns the Application Context based on the industry selected'''

    filepath = f"applicationcontext/{industry}.txt"
    applicationcontext = ""
    with open(filepath, 'r', encoding='utf-8') as file:
        applicationcontext = file.read()
    return applicationcontext