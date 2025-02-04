
import json
import os 
import ast
import msal
import logging
import traceback




def get_config_path():
    this_file_path = os.path.abspath(os.path.dirname(__file__))
    sep = os.path.sep
    config_file_path = os.path.join(
        this_file_path + sep + 'app.json')
    return config_file_path

def get_app_json():
    config_json_path = get_config_path()
    with open(config_json_path,'r',encoding='utf-8') as f:
        content = f.read()
        return json.loads(content)

app_json = get_app_json()
