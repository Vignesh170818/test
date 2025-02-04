'''Orchestration for Text Completion'''
import logging
from coreengine.textcompletion.azurecompletion import AzureGPT35Completion, AzureGPT4Completion
from coreengine.textcompletion.googlecompletion import GoogleBisonCompletion, GoogleGeminiCompletion
from coreengine.textcompletion.awscompletion import AWSTitanCompletion

logger=logging.getLogger("GenLiteApp")

class GenliteCompletion:
    '''Class for Generating SDLC Artifacts'''

    def __init__(self, llmplatform):
        '''Constructor'''

        self.llmplatform = llmplatform
        logger.info("GenliteCompletion init for %s", self.llmplatform)
        print(f"LLM Model Selected: {self.llmplatform}")
        self.completionmodel = None
        if self.llmplatform == "azureopenai":
            logger.info("Azure OpenAI GPT 3.5")
            self.completionmodel = AzureGPT35Completion()
        if self.llmplatform == "azureopenaigpt4":
            logger.info("Azure OpenAI GPT 4")
            self.completionmodel = AzureGPT4Completion()
        if self.llmplatform == "geminipro":
            logger.info("Gemini Pro")
            self.completionmodel = GoogleGeminiCompletion()
        if self.llmplatform == "textbison":
            logger.info("Text Bison")
            self.completionmodel = GoogleBisonCompletion()
        if self.llmplatform == "awstitan":
            logger.info("AWS Titan")
            self.completionmodel = AWSTitanCompletion()

    def generate_artifact(self, systemprompt):
        '''Generate Artifact'''
        logger.info("Generating Artifact")
        returnresponse = None

        if self.completionmodel is not None:
            returnresponse = self.completionmodel.generate(systemprompt)
        else:
            logger.error("LLM Model not supported. Please select a valid LLM Model.")

        return returnresponse

    async def generate_artifact_async(self, systemprompt):
        '''Generate Artifact'''
        logger.info("Generating Artifact")
        returnresponse = None

        if self.completionmodel is not None:
            returnresponse = await self.completionmodel.generate_async(
                systemprompt
                )
        else:
            logger.error("LLM Model not supported. Please select a valid LLM Model.")

        return returnresponse
