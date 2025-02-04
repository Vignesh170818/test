'''This module orchestrates the generation, review and application of the review of the EPIC'''
import asyncio
import logging
from appext.models.form import GenLiteMainForm
from plugins.architectureservice.controller import GenLiteArchitecture
from plugins.architectureservice.model import ArchitectureInput

logger=logging.getLogger("GenLiteApp")

async def generate_architecture(form: GenLiteMainForm):
    '''Orchestrates the generation of the EPIC'''
    logger.info("Orchestrating the generation of Architecture")
    llmplatform = form.llm_platform_options.data

    tasks = []

    if form.uiarchcheck.data is True:
        uiarchobject = GenLiteArchitecture(
        llmplatform=llmplatform
        )
        uiinputobject = ArchitectureInput()
        uiinputobject.platform = form.platform_choice.data
        uiinputobject.applicationcontext = form.ecosystem_context.data
        typeofarchitecture = "ui"
        uiinputobject.design = form.ui_detailed_design.data
        task_ui = asyncio.to_thread(
            uiarchobject.architecture_generate,
            typeofarchitecture,
            uiinputobject
            )
        tasks.append(task_ui)

    if form.servicesarchcheck.data is True:
        apiarchobject = GenLiteArchitecture(
        llmplatform=llmplatform
        )
        apiinputobject = ArchitectureInput()
        apiinputobject.platform = form.platform_choice.data
        apiinputobject.applicationcontext = form.ecosystem_context.data
        typeofarchitecture = "services"
        apiinputobject.design = form.services_detailed_design.data
        task_services = asyncio.to_thread(
            apiarchobject.architecture_generate,
            typeofarchitecture,
            apiinputobject
            )
        tasks.append(task_services)

    if form.dataarchcheck.data is True:
        dbarchobject = GenLiteArchitecture(
        llmplatform=llmplatform
        )
        dbinputobject = ArchitectureInput()
        dbinputobject.platform = form.platform_choice.data
        dbinputobject.applicationcontext = form.ecosystem_context.data
        typeofarchitecture = "data"
        dbinputobject.design = form.data_detailed_design.data
        tasks_data = asyncio.to_thread(
            dbarchobject.architecture_generate,
            typeofarchitecture,
            dbinputobject
            )
        tasks.append(tasks_data)

    results = await asyncio.gather(*tasks)
    uiarch = ""
    servicesarch = ""
    dataarch = ""

    # Assign results based on what options were selected
    result_index = 0
    if form.uiarchcheck.data is True:
        uiarch = results[result_index]
        result_index += 1

    if form.servicesarchcheck.data is True:
        servicesarch = results[result_index]
        result_index += 1

    if form.dataarchcheck.data is True:
        dataarch = results[result_index]
        result_index += 1

    returndict = {
        "uiarch":uiarch,
        "servicesarch":servicesarch,
        "dataarch":dataarch
        }
    logger.info("Architecture generation completed successfully")
    return returndict
