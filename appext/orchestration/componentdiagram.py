'''This module orchestrates the generation, review and application of the review of the EPIC'''
import asyncio
import logging
from appext.models.form import GenLiteMainForm
from plugins.componentdiagramservice.controller import GenLiteComponentDiagram
from plugins.componentdiagramservice.model import ComponentDiagramInput

logger=logging.getLogger("GenLiteApp")

async def generate_componentdiagram(form: GenLiteMainForm):
    '''Orchestrates the generation of the Component Diagram'''
    logger.info("Orchestrating the generation of the Component Diagram")
    llmplatform = form.llm_platform_options.data

    componentdiagramobject = GenLiteComponentDiagram(
    llmplatform=llmplatform
    )
    componentdiagraminputobject = ComponentDiagramInput()
    componentdiagraminputobject.applicationcontext = form.ecosystem_context.data
    componentdiagraminputobject.architecture = form.architecture_services.data
    componentdiagraminputobject.design = form.services_detailed_design.data
    componentdiagram = await asyncio.to_thread(
        componentdiagramobject.generate,
        componentdiagraminputobject
        )
    componentdiagram = componentdiagram.replace("```mermaid","")
    componentdiagram = componentdiagram.replace("```","")
    componentdiagram = componentdiagram.replace("mermaid\n","")
    componentdiagram = componentdiagram.replace("\n\n","\n")
    logger.info("Component Diagram generation completed successfully")
    return componentdiagram
