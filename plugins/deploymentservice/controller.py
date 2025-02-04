'''This is the controller for the deployment service plugin.'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.deploymentservice.model import (
    DeploymentInput
)

class GenLiteDeployment:
    '''Class for Deployment Service'''

    def __init__(
            self,
            llmplatform="azureopenai"
            ):
        self.llmplatform = llmplatform
        self.completionmodel = GenliteCompletion(self.llmplatform)

    def deployment_generate(
            self,
            deploymentinputdata: DeploymentInput,
            platform: str
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer(f"deployment_{platform}")
        dictobject = {
            "architecture": deploymentinputdata.architecture,
            "design": deploymentinputdata.design
            }
        systemprompt = promptobject.render(**dictobject)
        deployment = self.completionmodel.generate_artifact(systemprompt)
        return deployment
