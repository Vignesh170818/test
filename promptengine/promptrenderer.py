'''
This file contains the PromptRenderer class.
This focuses on using Jinja2 to render a Prompt template.
'''
import logging
import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound, TemplateSyntaxError, TemplateError

logger=logging.getLogger("GenLiteApp")

class PromptRenderer:
    """
    Render a prompt template.
    """
    def __init__(self, type_of_template):
        # Load configuration
        self.configfilepath = 'promptengine/config.yaml'
        self.config = self.load_config(self.configfilepath)

        # Extract the configuration for the given template type
        template_config = self.config.get(type_of_template, {})
        self.template_dir = template_config.get('template_dir', '')
        self.template_name = template_config.get('template_name', '')

        # Initialize the environment
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def load_config(self, config_path='config.yaml'):
        """Load the configuration file."""
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return yaml.safe_load(config_file)

    def render(self, **kwargs):
        """Render the template."""
        try:
            template = self.env.get_template(self.template_name)
            return template.render(**kwargs)  # Ensure kwargs is unpacked here
        except TemplateNotFound as e:
            logger.error("Error: template not found: %s", e)
            return ""
        except TemplateSyntaxError as e:
            logger.error("Error: template syntax error: %s", e)
            return ""
        except TemplateError as e:
            logger.error("Error: template error: %s")
            return ""

    # Render from a dictionary
    def render_from_dict(self, data):
        """Render from a dictionary."""
        try:
            template = self.env.get_template(self.template_name)
            return template.render(data)
        except TemplateNotFound as e:
            logger.error("Error: template not found: %s", e)
            return ""
        except TemplateSyntaxError as e:
            logger.error("Error: template syntax error: %s", e)
            return ""
        except TemplateError as e:
            logger.error("Error: template error: %s")
            return ""
