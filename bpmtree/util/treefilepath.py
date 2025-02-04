'''
This file contains the BPMFilePath class.
'''
import yaml

class BPMFilePath:
    """
    Render a prompt template.
    """

    def __load_config__(self, config_path='config.yaml'):
        """Load the configuration file."""
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return yaml.safe_load(config_file)

    def __init__(self, industry):
        # Load configuration
        self.configfilepath = 'bpmtree/util/config.yaml'
        self.config = self.__load_config__(self.configfilepath)

        # Extract the configuration for the given template type
        template_config = self.config.get(industry, {})
        self.indexfile_location = template_config.get('indexfile_location', '')
        self.treefile_location = template_config.get('treefile_location', '')

    def get_indexfile_location(self):
        '''Return the index file location.'''
        return self.indexfile_location

    def get_treefile_location(self):
        '''Return the tree file location.'''
        return self.treefile_location
