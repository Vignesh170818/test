'''This class is used to generate the Features and expand the features'''
import bleach
from genliteappext.genliteform import GenLiteMainForm
from genlite.tdlc.test import GenLiteTest

class TestGenerator:
    '''This class is used to generate the Features and expand the features'''

    def __init__(self, form: GenLiteMainForm, llmplatform="azureopenai"):
        self.genliteform = form
        self.promptpath="genlite/tdlc/prompts/test/"
        self.llmplatform = llmplatform
        #initialize variables
        self.industry = self.genliteform.industry.data
        self.designtype = ''
        self.applicationcontext = ''
        self.businesscontext = ''
        self.high_level_req = ''
        self.processflow = ''
        self.epic = ''
        self.feature = ''
        self.selected_user_story = ''
        self.functional_design = ''

        test_input_multi = self.genliteform.st_input_multi.data
        test_input = self.genliteform.st_key_input.data

        self.slicingcriteria = self.genliteform.slicingmethod.data

        if 'applicationcontext' in test_input_multi:
            self.applicationcontext = self.genliteform.ecosystem_context.data
            self.applicationcontext = bleach.clean(self.applicationcontext)

        if 'businesscontext' in test_input_multi:
            self.businesscontext = self.genliteform.business_process_mapping.data
            self.businesscontext = bleach.clean(self.businesscontext)

        if 'processflow' in test_input_multi:
            self.processflow = self.genliteform.process_flow_mapping.data
            self.processflow = bleach.clean(self.processflow)

        if 'scopevision' in test_input_multi:
            self.high_level_req = self.genliteform.scope_vision.data
            self.high_level_req = bleach.clean(self.high_level_req)

        if test_input == "epic":
            self.epic = self.genliteform.epic_user_story.data
            self.epic = bleach.clean(self.epic)

        if test_input == "feature":
            self.feature = self.genliteform.feature_user_story.data
            self.feature = bleach.clean(self.feature)

        if test_input == "userstory":
            combineuserstory = self.genliteform.selected_user_story.data
            combineuserstory += "\n"
            combineuserstory += self.genliteform.user_story_abstract.data
            self.selected_user_story = bleach.clean(combineuserstory)

        if test_input == "functional-ui":
            self.designtype = "UI"
            self.functional_design = self.genliteform.ui_functional_design.data
            self.functional_design = bleach.clean(self.functional_design)

        if test_input == "functional-services":
            self.designtype = "Services"
            self.functional_design = self.genliteform.services_functional_design.data
            self.functional_design = bleach.clean(self.functional_design)

        if test_input == "functional-data":
            self.designtype = "Data"
            self.functional_design = self.genliteform.data_functional_design.data
            self.functional_design = bleach.clean(self.functional_design)

        if self.genliteform.test_plan.data != "":
            self.test_plan = self.genliteform.test_plan.data
            self.test_plan = bleach.clean(self.test_plan)
        else:
            self.test_plan = ""

        if self.genliteform.test_cases.data != "":
            self.test_case = self.genliteform.test_cases.data
            self.test_case = bleach.clean(self.test_case)
        else:
            self.test_case = ""

        if self.genliteform.test_scripts.data != "":
            self.test_script = self.genliteform.test_scripts.data
            self.test_script = bleach.clean(self.test_script)
        else:
            self.test_script = ""

    def generate_test_plan(self):
        '''Function to generate the test plan'''
        testobj = GenLiteTest(
            industry=self.industry,
            promptpath=self.promptpath,
            llmplatform=self.llmplatform
            )
        testplan = testobj.generate_test_plan(
            application_context=self.applicationcontext,
            business_context=self.businesscontext,
            high_level_req=self.high_level_req,
            epic=self.epic,
            feature=self.feature,
            selecteduserstory=self.selected_user_story,
            functionaldesign=self.functional_design
            )
        return testplan

    def generate_test_case(self):
        '''Function to generate the test case'''
        testobj = GenLiteTest(
            industry=self.industry,
            promptpath=self.promptpath,
            llmplatform=self.llmplatform
            )
        testcase = testobj.generate_test_case(
            application_context=self.applicationcontext,
            business_context=self.businesscontext,
            high_level_req=self.high_level_req,
            epic=self.epic,
            feature=self.feature,
            selecteduserstory=self.selected_user_story,
            functionaldesign=self.functional_design,
            test_plan=self.test_plan
            )
        return testcase

    def generate_test_script(self):
        '''Function to generate the test script'''
        testobj = GenLiteTest(
            industry=self.industry,
            promptpath=self.promptpath,
            llmplatform=self.llmplatform
            )
        testscript = testobj.generate_test_scripts(
            application_context=self.applicationcontext,
            business_context=self.businesscontext,
            high_level_req=self.high_level_req,
            epic=self.epic,
            feature=self.feature,
            selecteduserstory=self.selected_user_story,
            functionaldesign=self.functional_design,
            test_plan=self.test_plan,
            test_case=self.test_case
            )
        return testscript

    def generate_test_scripts_for_tool(self):
        '''Function to generate the test script'''

        testobj = GenLiteTest(
            industry=self.industry,
            promptpath=self.promptpath,
            llmplatform=self.llmplatform
            )

        testscript = testobj.generate_scripts_for_tool(
            application_context=self.applicationcontext,
            business_context=self.businesscontext,
            high_level_req=self.high_level_req,
            epic=self.epic,
            feature=self.feature,
            selecteduserstory=self.selected_user_story,
            functionaldesign=self.functional_design,
            test_plan=self.test_plan,
            test_case=self.test_case,
            test_scripts=self.test_script,
            system_test_tools=self.genliteform.system_test_tool.data
            )
        return testscript
