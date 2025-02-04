'''LLMManager class for managing LLM models'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.designservice.model import (
    FunctionalDesignInput,
    HighLevelDesignInput,
    LowLevelDesignInput)
from bpmtree.util.industry import GenLiteIndustry

class GenLiteDesign:
    '''Class for Design Service'''

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

    def generate_functional_design(
            self,
            designtype: str,
            fdinputdata: FunctionalDesignInput
            ):
        '''Generate a functional design for given business context'''

        promptobject = PromptRenderer(f"functionaldesign_{designtype}")

        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": fdinputdata.businesscontext,
            "highlevelreq": fdinputdata.highlevelreq,
            "applicationcontext": fdinputdata.applicationcontext,
            "processflow": fdinputdata.processflow,
            "epic": fdinputdata.epic,
            "feature": fdinputdata.feature,
            "userstory": fdinputdata.userstory
            }
        systemprompt = promptobject.render(**dictobject)
        functionaldesign = self.completionmodel.generate_artifact(systemprompt)
        return functionaldesign

    def generate_high_level_design(
            self,
            designtype: str,
            hldinputdata: HighLevelDesignInput
            ):
        '''Generate a high level design for given business context'''

        promptobject = PromptRenderer(f"highleveldesign_{designtype}")

        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": hldinputdata.businesscontext,
            "highlevelreq": hldinputdata.highlevelreq,
            "applicationcontext": hldinputdata.applicationcontext,
            "processflow": hldinputdata.processflow,
            "epic": hldinputdata.epic,
            "feature": hldinputdata.feature,
            "userstory": hldinputdata.userstory,
            "functionaldesign": hldinputdata.functionaldesign
            }
        systemprompt = promptobject.render(**dictobject)
        highleveldesign = self.completionmodel.generate_artifact(systemprompt)
        return highleveldesign

    def generate_low_level_design(
            self,
            designtype: str,
            lldinputdata: LowLevelDesignInput,
            ):
        '''Generate a low level design for given business context'''

        promptobject = PromptRenderer(f"lowleveldesign_{designtype}")

        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": lldinputdata.businesscontext,
            "highlevelreq": lldinputdata.highlevelreq,
            "applicationcontext": lldinputdata.applicationcontext,
            "processflow": lldinputdata.processflow,
            "epic": lldinputdata.epic,
            "feature": lldinputdata.feature,
            "userstory": lldinputdata.userstory,
            "functionaldesign": lldinputdata.functionaldesign,
            "highleveldesign": lldinputdata.highleveldesign
            }
        systemprompt = promptobject.render(**dictobject)
        lowleveldesign = self.completionmodel.generate_artifact(systemprompt)
        return lowleveldesign
