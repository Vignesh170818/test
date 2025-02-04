'''Controller for the component diagram service plugin. 
This plugin is used to generate component diagrams for a given business context'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.componentdiagramservice.model import (
    ComponentDiagramInput
)

class GenLiteComponentDiagram:
    '''Class for Component Diagram Service'''

    def __init__(
            self,
            llmplatform="azureopenai"
            ):
        self.llmplatform = llmplatform
        self.completionmodel = GenliteCompletion(self.llmplatform)

    def generate(
            self,
            componentdiagraminputdata: ComponentDiagramInput
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("componentdiagram")
        dictobject = {
            "applicationcontext": componentdiagraminputdata.applicationcontext,
            "architecture": componentdiagraminputdata.architecture,
            "design": componentdiagraminputdata.design
            }
        systemprompt = promptobject.render(**dictobject)
        componentdiagram = self.completionmodel.generate_artifact(systemprompt)
        componentdiagram = componentdiagram.replace("\n\n","\n")
        componentdiagram = componentdiagram.replace("**","")
        componentdiagram = componentdiagram.replace("```","")
        return componentdiagram
