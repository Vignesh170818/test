'''LLMManager class for managing LLM models'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.featureservice.model import FeatureInput, ExpandFeatureInput
from bpmtree.util.industry import GenLiteIndustry

class GenLiteFeature:
    '''Class for Feature Service'''

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
            featureinputdata: FeatureInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("generatefeature")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": featureinputdata.businesscontext,
            "highlevelreq": featureinputdata.highlevelreq,
            "applicationcontext": featureinputdata.applicationcontext,
            "processflow": featureinputdata.processflow,
            "epic": featureinputdata.epic
            }
        systemprompt = promptobject.render(**dictobject)
        feature = self.completionmodel.generate_artifact(systemprompt)
        return feature

    def expand(
            self,
            featureinputdata: ExpandFeatureInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("expandfeature")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": featureinputdata.businesscontext,
            "highlevelreq": featureinputdata.highlevelreq,
            "applicationcontext": featureinputdata.applicationcontext,
            "processflow": featureinputdata.processflow,
            "epic": featureinputdata.epic,
            "feature": featureinputdata.feature
            }
        systemprompt = promptobject.render(**dictobject)
        feature = self.completionmodel.generate_artifact(systemprompt)
        return feature
