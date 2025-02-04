'''LLMManager class for managing LLM models'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.bpmservice.model import BPMInput
from bpmtree.util.industry import GenLiteIndustry

class GenLiteBPM:
    '''Class for Generating BPM Diagrams in mermaid'''

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

    def processflow_generate(
            self,
            bpminputdata: BPMInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("processflow")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": bpminputdata.businesscontext
            }
        systemprompt = promptobject.render(**dictobject)
        processflow = self.completionmodel.generate_artifact(systemprompt)
        processflow = processflow.replace("\n\n","\n")
        processflow = processflow.replace("**","")
        processflow = processflow.replace("```","")
        return processflow

    async def processflow_generate_async(
            self,
            bpminputdata: BPMInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("processflow")
        dictobject = {
            "industry": self.industrylabel,
            "businesscontext": bpminputdata.businesscontext
            }
        systemprompt = promptobject.render(**dictobject)
        processflow = await self.completionmodel.generate_artifact(
            systemprompt
            )
        processflow = processflow.replace("\n\n","\n")
        processflow = processflow.replace("**","")
        processflow = processflow.replace("```","")
        return processflow

    def bpmjson_generate(
            self,
            bpminputdata: BPMInput
            ):
        '''Generate BPM context for given high level requirements and application context'''

        promptobject = PromptRenderer("bpmjson")
        dictobject = {
            "industry": self.industrylabel,
            "highlevelreq": bpminputdata.highlevelreq,
            "applicationcontext": bpminputdata.applicationcontext
            }
        systemprompt = promptobject.render(**dictobject)
        generatedbpm = self.completionmodel.generate_artifact(systemprompt)

        generatedbpm = generatedbpm.replace("\n\n","\n")
        generatedbpm = generatedbpm.replace("**","")
        generatedbpm = generatedbpm.replace("```json","")
        generatedbpm = generatedbpm.replace("```","")

        return generatedbpm

    async def bpmjson_generate_async(
            self,
            bpminputdata: BPMInput
            ):
        '''Generate BPM context for given high level requirements and application context'''

        promptobject = PromptRenderer("bpmjson")
        dictobject = {
            "industry": self.industrylabel,
            "highlevelreq": bpminputdata.highlevelreq,
            "applicationcontext": bpminputdata.applicationcontext
            }
        systemprompt = promptobject.render(**dictobject)
        generatedbpm = await self.completionmodel.generate_artifact_async(systemprompt)

        generatedbpm = generatedbpm.replace("\n\n","\n")
        generatedbpm = generatedbpm.replace("**","")
        generatedbpm = generatedbpm.replace("```json","")
        generatedbpm = generatedbpm.replace("```","")

        return generatedbpm
