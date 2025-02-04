'''This class is used to generate the Features and expand the features'''
import bleach
from genliteappext.genliteform import GenLiteMainForm
from genliteappext.utils import validate_length
from genlite.tdlc.userstory import GenLiteUserStory

class UserStoryGenerator:
    '''This class is used to generate the Features and expand the features'''

    def __init__(self, form: GenLiteMainForm, llmplatform="azureopenai"):
        self.genliteform = form
        self.promptpath="genlite/tdlc/prompts/"
        self.llmplatform = llmplatform
        #initialize variables
        self.epic = ''
        self.feature = ''
        self.applicationcontext = ''
        self.businesscontext = ''
        self.processflow = ''
        self.scope_vision = ''
        self.industry = self.genliteform.industry.data
        userstoriesmulti = self.genliteform.userstories_input_multi.data
        combineuserstory = self.genliteform.selected_user_story.data
        combineuserstory += "\n"
        combineuserstory += self.genliteform.user_story_abstract.data
        self.selected_user_story = combineuserstory
        self.slicingcriteria = self.genliteform.slicingmethod.data

        if 'applicationcontext' in userstoriesmulti:
            self.applicationcontext = self.genliteform.ecosystem_context.data
            self.applicationcontext = bleach.clean(self.applicationcontext)

        if 'businesscontext' in userstoriesmulti:
            self.businesscontext = self.genliteform.business_process_mapping.data
            self.businesscontext = bleach.clean(self.businesscontext)

        if 'processflow' in userstoriesmulti:
            self.processflow = self.genliteform.process_flow_mapping.data
            self.processflow = bleach.clean(self.processflow)

        if 'scopevision' in userstoriesmulti:
            self.scope_vision = self.genliteform.scope_vision.data
            self.scope_vision = bleach.clean(self.scope_vision)

        if 'epic' in userstoriesmulti:
            self.epic = self.genliteform.epic_user_story.data
            self.epic = bleach.clean(self.epic)

        if 'feature' in userstoriesmulti:
            self.feature = self.genliteform.feature_user_story.data
            self.feature = bleach.clean(self.feature)

    def generate_userstory(self):
        '''Process the request and return the results'''

        is_valid=validate_length(
            self.industry,
            self.applicationcontext,
            self.businesscontext,
            self.processflow,
            self.scope_vision
            )

        if is_valid:
            #generate the feature
            userstory = GenLiteUserStory(
                self.industry,
                self.promptpath,
                self.llmplatform
                )

            userstorycontent = userstory.generate_userstory(
                application_context=self.applicationcontext,
                business_context=self.businesscontext,
                process_flow=self.processflow,
                high_level_req=self.scope_vision,
                epic=self.epic,
                feature=self.feature,
                slicing_criteria=self.slicingcriteria
                )
            return userstorycontent
        else:
            return "Invalid Input"

    def expand_user_story(self):
        '''Process the request and return the results'''

        is_valid=validate_length(
            self.industry,
            self.applicationcontext,
            self.businesscontext,
            self.processflow,
            self.scope_vision
            )

        if is_valid:
            #generate the feature
            userstory = GenLiteUserStory(
                self.industry,
                self.promptpath,
                self.llmplatform
                )

            userstorycontent = userstory.expand_userstory(
                application_context=self.applicationcontext,
                business_context=self.businesscontext,
                high_level_req=self.scope_vision,
                epic=self.epic,
                feature=self.feature,
                selecteduserstory=self.selected_user_story
                )
            return userstorycontent
        else:
            return "Invalid Input"

    def generate_tasks(self):
        '''Process the request and return the results'''

        is_valid=validate_length(
            self.industry,
            self.applicationcontext,
            self.businesscontext,
            self.processflow,
            self.scope_vision
            )

        if is_valid:
            #generate the feature
            userstory = GenLiteUserStory(
                self.industry,
                self.promptpath,
                self.llmplatformadvanced
                )

            userstorycontent = userstory.generate_tasks(
                application_context=self.applicationcontext,
                business_context=self.businesscontext,
                high_level_req=self.scope_vision,
                epic=self.epic,
                feature=self.feature,
                selecteduserstory=self.selected_user_story
                )
            return userstorycontent
        else:
            return "Invalid Input"
