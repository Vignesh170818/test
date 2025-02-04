'''Controller for the architecture service plugin'''

from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.architectureservice.model import (
    ArchitectureInput
)

class GenLiteArchitecture:
    '''Class for Architecture Service'''

    def __init__(
            self,
            llmplatform="azureopenai"
            ):
        self.llmplatform = llmplatform
        self.completionmodel = GenliteCompletion(self.llmplatform)

    def architecture_generate(
            self,
            typeofarchitecture: str,
            architectureinputdata: ArchitectureInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer(f"architecture_{typeofarchitecture}")
        dictobject = {
            "platform": architectureinputdata.platform,
            "applicationcontext": architectureinputdata.applicationcontext,
            "design": architectureinputdata.design
            }
        systemprompt = promptobject.render(**dictobject)
        architecture = self.completionmodel.generate_artifact(systemprompt)
        architecture = architecture.replace("\n\n","\n")
        architecture = architecture.replace("**","")
        architecture = architecture.replace("```","")
        return architecture
