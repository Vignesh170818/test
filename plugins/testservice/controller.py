'''Controller for the test service plugin'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.testservice.model import (
    TestScenariosInput,
    TestCasesInput,
    TestScriptsInput,
    ToolTestScriptsInput
)
from bpmtree.util.industry import GenLiteIndustry

class GenLiteTest:
    '''Class for Test Service'''

    def __init__(
            self,
            industry,
            llmplatform="azureopenai"
            ):
        self.industry = industry
        self.llmplatform = llmplatform
        self.industrylabel = GenLiteIndustry().get_industry_label(
            industry
            )
        self.combinedbusinesscontext = ""
        self.completionmodel = GenliteCompletion(self.llmplatform)

    def generate_test_scenarios(
            self,
            input_data: TestScenariosInput
            ):
        '''Generates test scenarios'''

        dictobject = {
            "businesscontext": input_data.businesscontext,
            "highlevelreq": input_data.highlevelreq,
            "applicationcontext": input_data.applicationcontext,
            "processflow": input_data.processflow,
            "epic": input_data.epic,
            "feature": input_data.feature,
            "userstory": input_data.userstory,
            "functionaldesignui": input_data.functionaldesignui,
            "functionaldesignservices": input_data.functionaldesignservices,
            "functionaldesigndata": input_data.functionaldesigndata
        }
        promptobject = PromptRenderer("testscenarios")
        systemprompt = promptobject.render(**dictobject)
        testscenarios = self.completionmodel.generate_artifact(systemprompt)
        return testscenarios

    def generate_test_cases(
            self,
            input_data: TestCasesInput
            ):
        '''Generates test cases'''

        dictobject = {
            "businesscontext": input_data.businesscontext,
            "highlevelreq": input_data.highlevelreq,
            "applicationcontext": input_data.applicationcontext,
            "processflow": input_data.processflow,
            "epic": input_data.epic,
            "feature": input_data.feature,
            "userstory": input_data.userstory,
            "functionaldesignui": input_data.functionaldesignui,
            "functionaldesignservices": input_data.functionaldesignservices,
            "functionaldesigndata": input_data.functionaldesigndata,
            "testscenario": input_data.testscenario
        }
        promptobject = PromptRenderer("testcases")
        systemprompt = promptobject.render(**dictobject)
        testcases = self.completionmodel.generate_artifact(systemprompt)
        return testcases

    def generate_test_scripts(
            self,
            input_data: TestScriptsInput
            ):
        '''Generates test scripts'''

        dictobject = {
            "businesscontext": input_data.businesscontext,
            "highlevelreq": input_data.highlevelreq,
            "applicationcontext": input_data.applicationcontext,
            "processflow": input_data.processflow,
            "epic": input_data.epic,
            "feature": input_data.feature,
            "userstory": input_data.userstory,
            "functionaldesignui": input_data.functionaldesignui,
            "functionaldesignservices": input_data.functionaldesignservices,
            "functionaldesigndata": input_data.functionaldesigndata,
            "testscenario": input_data.testscenario,
            "testcase": input_data.testcase
        }
        promptobject = PromptRenderer("testscripts")
        systemprompt = promptobject.render(**dictobject)
        testscripts = self.completionmodel.generate_artifact(systemprompt)
        return testscripts

    def generate_tool_test_scripts(
            self,
            input_data: ToolTestScriptsInput
            ):
        '''Generates tool test scripts'''

        dictobject = {
            "businesscontext": input_data.businesscontext,
            "highlevelreq": input_data.highlevelreq,
            "applicationcontext": input_data.applicationcontext,
            "processflow": input_data.processflow,
            "epic": input_data.epic,
            "feature": input_data.feature,
            "userstory": input_data.userstory,
            "functionaldesignui": input_data.functionaldesignui,
            "functionaldesignservices": input_data.functionaldesignservices,
            "functionaldesigndata": input_data.functionaldesigndata,
            "testscenario": input_data.testscenario,
            "testcase": input_data.testcase,
            "testscript": input_data.testscript,
            "tool": input_data.tool
        }
        promptobject = PromptRenderer(f"testscripts_{input_data.tool.lower()}")
        systemprompt = promptobject.render(**dictobject)
        tooltestscripts = self.completionmodel.generate_artifact(systemprompt)
        return tooltestscripts
