'''LLMManager class for managing LLM models'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.epicservice.model import EPICInput, EPICReviewInput, EPICApplyReviewInput
from bpmtree.util.industry import GenLiteIndustry

class GenLiteEPIC:
    '''Class for EPIC Service'''

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

    def generate(
            self,
            epicinputdata: EPICInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("generateepic")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": epicinputdata.businesscontext,
            "highlevelreq": epicinputdata.highlevelreq,
            "applicationcontext": epicinputdata.applicationcontext
            }
        systemprompt = promptobject.render(**dictobject)
        processflow = self.completionmodel.generate_artifact(systemprompt)
        processflow = processflow.replace("\n\n","\n")
        processflow = processflow.replace("**","")
        processflow = processflow.replace("```","")
        return processflow

    def review(
            self,
            epicinputdata: EPICReviewInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("reviewepic")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": epicinputdata.businesscontext,
            "highlevelreq": epicinputdata.highlevelreq,
            "applicationcontext": epicinputdata.applicationcontext,
            "epic": epicinputdata.epic
            }
        systemprompt = promptobject.render(**dictobject)
        processflow = self.completionmodel.generate_artifact(systemprompt)
        processflow = processflow.replace("\n\n","\n")
        processflow = processflow.replace("**","")
        processflow = processflow.replace("```","")
        return processflow

    def applyreview(
            self,
            epicinputdata: EPICApplyReviewInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("applyepicreview")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": epicinputdata.businesscontext,
            "highlevelreq": epicinputdata.highlevelreq,
            "applicationcontext": epicinputdata.applicationcontext,
            "epic": epicinputdata.epic,
            "reviewcomments": epicinputdata.reviewcomments
            }
        systemprompt = promptobject.render(**dictobject)
        processflow = self.completionmodel.generate_artifact(systemprompt)
        if processflow is None:
            processflow = "No changes"
        else:
            processflow = processflow.replace("\n\n","\n")
            processflow = processflow.replace("**","")
            processflow = processflow.replace("```","")
        return processflow
