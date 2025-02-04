'''Controller for Code Service'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.codeservice.model import (
    CodeInput
)
from bpmtree.util.industry import GenLiteIndustry

class GenLiteCode:
    '''Class for Code Service'''

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
            codeinputdata: CodeInput,
            typeofcode: str,
            programminglanguage: str
            ):
        '''Generate a process flow for given business context'''
        print(f"codegeneration_{typeofcode}_{programminglanguage}")
        promptobject = PromptRenderer(f"codegeneration_{typeofcode}_{programminglanguage}")

        dictobject = {
            "industry": self.industrylabel,
            "applicationcontext": codeinputdata.applicationcontext,
            "highleveldesign": codeinputdata.highleveldesign,
            "lowleveldesign": codeinputdata.lowleveldesign
            }
        systemprompt = promptobject.render(**dictobject)
        code = self.completionmodel.generate_artifact(systemprompt)
        return code

    def review(
            self,
            codeinputdata: CodeInput,
            typeofcode: str,
            programminglanguage: str
            ):
        '''Review the generated code'''

        promptobject = PromptRenderer(f"codereview_{typeofcode}_{programminglanguage}")

        dictobject = {
            "industry": self.industrylabel,
            "applicationcontext": codeinputdata.applicationcontext,
            "highleveldesign": codeinputdata.highleveldesign,
            "lowleveldesign": codeinputdata.lowleveldesign
            }
        systemprompt = promptobject.render(**dictobject)
        review = self.completionmodel.generate_artifact(systemprompt)
        return review
    
    def apply(
            self,
            codeinputdata: CodeInput,
            typeofcode: str,
            programminglanguage: str
            ):
        '''Apply the generated code'''

        promptobject = PromptRenderer(f"codeapply_{typeofcode}_{programminglanguage}")

        dictobject = {
            "industry": self.industrylabel,
            "applicationcontext": codeinputdata.applicationcontext,
            "highleveldesign": codeinputdata.highleveldesign,
            "lowleveldesign": codeinputdata.lowleveldesign
            }
        systemprompt = promptobject.render(**dictobject)
        apply = self.completionmodel.generate_artifact(systemprompt)
        return apply
