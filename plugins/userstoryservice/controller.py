'''LLMManager class for managing LLM models'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.userstoryservice.model import UserStoryInput, ExpandUserStoryInput
from bpmtree.util.industry import GenLiteIndustry

class GenLiteUserStory:
    '''Class for User Story Service'''

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
        self.completionmodel = GenliteCompletion(self.llmplatform)

    def generate(
            self,
            typeofslicing: str,
            userstoryinputdata: UserStoryInput
            ):
        '''Generate a process flow for given business context'''

        promptobject = PromptRenderer(f"userstories_{typeofslicing}")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": userstoryinputdata.businesscontext,
            "highlevelreq": userstoryinputdata.highlevelreq,
            "applicationcontext": userstoryinputdata.applicationcontext,
            "processflow": userstoryinputdata.processflow,
            "epic": userstoryinputdata.epic,
            "feature": userstoryinputdata.feature
            }
        systemprompt = promptobject.render(**dictobject)
        userstory = self.completionmodel.generate_artifact(systemprompt)
        return userstory

    def expand(
            self,
            userstoryinputdata: ExpandUserStoryInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("expanduserstory")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": userstoryinputdata.businesscontext,
            "highlevelreq": userstoryinputdata.highlevelreq,
            "applicationcontext": userstoryinputdata.applicationcontext,
            "processflow": userstoryinputdata.processflow,
            "epic": userstoryinputdata.epic,
            "feature": userstoryinputdata.feature,
            "userstory": userstoryinputdata.userstory
            }
        systemprompt = promptobject.render(**dictobject)
        userstory = self.completionmodel.generate_artifact(systemprompt)
        return userstory

    def generate_tasks(
            self,
            userstoryinputdata: ExpandUserStoryInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("userstorytasks")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": userstoryinputdata.businesscontext,
            "highlevelreq": userstoryinputdata.highlevelreq,
            "applicationcontext": userstoryinputdata.applicationcontext,
            "processflow": userstoryinputdata.processflow,
            "epic": userstoryinputdata.epic,
            "feature": userstoryinputdata.feature,
            "userstory": userstoryinputdata.userstory
            }
        systemprompt = promptobject.render(**dictobject)
        userstory = self.completionmodel.generate_artifact(systemprompt)
        return userstory
