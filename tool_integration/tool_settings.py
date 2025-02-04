import logging
import os
import yaml
from configparser import ConfigParser, ExtendedInterpolation

module_logger = logging.getLogger("tool_integration.settings")

def get_config_path():
    module_logger.info(f"Method 'get_config_path()' started")
    this_file_path = os.path.abspath(os.path.dirname(__file__))
    configfilepath = os.path.join(this_file_path, 'config.yaml')

    with open(configfilepath, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

    tool_entity_config = {'tool_entity': config.get('tool_entity', {})}
    return tool_entity_config

config_f_path = get_config_path()
