'''Controller for the architecture service plugin'''
from coreengine.multimodal.googlevision import GoogleVisionCompletionModel
from promptengine.promptrenderer import PromptRenderer

class GenLiteDesignFromImage:
    '''Class for Architecture Service'''

    def __init__(
            self,
            imagefilepath,
            llmplatform="azureopenai",
            ):
        self.imagefilepath = imagefilepath
        self.llmplatform = llmplatform

    def __genereate_image_using_google_vision(self, systemprompt):
        '''Generate the functional design using Google Vision API'''
        googlevision = GoogleVisionCompletionModel()
        # systemprompt = "Generate functional design from the given image"
        functional_design = googlevision.generate(
            self.imagefilepath,
            systemprompt
            )
        return functional_design

    def generate_functional_design(
            self
            ):
        '''Generate a process flow for given business context'''
        promptobject = PromptRenderer("functionaldesign_image")
        systemprompt = promptobject.render()
        functional_design = self.__genereate_image_using_google_vision(systemprompt)
        return functional_design
