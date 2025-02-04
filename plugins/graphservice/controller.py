'''Controller for the architecture service plugin'''
from coreengine.textcompletion.orchestration import GenliteCompletion
from promptengine.promptrenderer import PromptRenderer
from plugins.graphservice.model import GraphInput


class GenLiteGenerateGraph:
    '''Class for Architecture Service'''

    def __init__(
            self,
            llmplatform="azureopenai"
            ):
        self.completionmodel = GenliteCompletion(llmplatform)

    def generate(
            self,
            inputdata: GraphInput
            ):
        '''Generate a graph for given code'''
        
        sourcecodelang = inputdata.graphsourcecodelang

        dictobject = {
            "sourcecode": inputdata.graphsourcecode,
            "uniqueId" :inputdata.uniqueId
            }

        promptobject = PromptRenderer(f"graph_{sourcecodelang}")
        systemprompt = promptobject.render(**dictobject)
        
        if systemprompt == "":
            cypherquery = "Graph Conversion not supported for the given source languages."
        else:
            cypherquery = self.completionmodel.generate_artifact(systemprompt)
            
        return cypherquery
            

    