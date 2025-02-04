'''Orchestrates the generation of the Feature'''
import asyncio
import logging
from appext.models.form import GenLiteMainForm
from plugins.designservice.controller import GenLiteDesign
from plugins.designservice.model import (
    FunctionalDesignInput,
    HighLevelDesignInput,
    LowLevelDesignInput
    )
from plugins.designfromimageservice.controller import GenLiteDesignFromImage

logger=logging.getLogger("GenLiteApp")

async def generate_functional_design(form: GenLiteMainForm):
    '''Orchestrates the generation of the Functional Design'''
    logger.info("Orchestrating the generation of the Functional Design")
    llmplatform = form.llm_platform_options.data

    tasks = []

    if form.uifuncdesigncheck.data is True:
        designui = GenLiteDesign(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
        inputui = FunctionalDesignInput()

        uimulti = form.fd_input_multi.data

        if "applicationcontext" in uimulti:
            inputui.applicationcontext = form.ecosystem_context.data
        if "businesscontext" in uimulti:
            inputui.businesscontext = form.business_process_mapping.data
        if "processflow" in uimulti:
            inputui.processflow = form.process_flow_mapping.data

        if form.fd_input.data == "epic":
            inputui.epic = form.epic_user_story.data
        if form.fd_input.data == "feature":
            inputui.feature = form.feature_user_story.data
        if form.fd_input.data == "userstory":
            userstory = form.selected_user_story.data
            userstory += "\n"
            userstory += form.user_story_abstract.data
            inputui.userstory = userstory
        if form.fd_input.data == "scopevision":
            inputui.highlevelreq = form.scope_vision.data

        uitask = asyncio.to_thread(
            designui.generate_functional_design,
            "ui",
            inputui
            )
        tasks.append(uitask)

    if form.servicesfuncdesigncheck.data is True:
        designservices = GenLiteDesign(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
        inputservices = FunctionalDesignInput()

        servicesmulti = form.fd_input_multi.data

        if "applicationcontext" in servicesmulti:
            inputservices.applicationcontext = form.ecosystem_context.data
        if "businesscontext" in servicesmulti:
            inputservices.businesscontext = form.business_process_mapping.data
        if "processflow" in servicesmulti:
            inputservices.processflow = form.process_flow_mapping.data

        if form.fd_input.data == "epic":
            inputservices.epic = form.epic_user_story.data
        if form.fd_input.data == "feature":
            inputservices.feature = form.feature_user_story.data
        if form.fd_input.data == "userstory":
            userstory = form.selected_user_story.data
            userstory += "\n"
            userstory += form.user_story_abstract.data
            inputservices.userstory = userstory
        if form.fd_input.data == "scopevision":
            inputservices.highlevelreq = form.scope_vision.data

        servicestask = asyncio.to_thread(
            designservices.generate_functional_design,
            "services",
            inputservices
            )
        tasks.append(servicestask)

    if form.datafuncdesigncheck.data is True:
        designdata = GenLiteDesign(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
        inputdata = FunctionalDesignInput()

        datamulti = form.fd_input_multi.data

        if "applicationcontext" in datamulti:
            inputdata.applicationcontext = form.ecosystem_context.data
        if "businesscontext" in datamulti:
            inputdata.businesscontext = form.business_process_mapping.data
        if "processflow" in datamulti:
            inputdata.processflow = form.process_flow_mapping.data

        if form.fd_input.data == "epic":
            inputdata.epic = form.epic_user_story.data
        if form.fd_input.data == "feature":
            inputdata.feature = form.feature_user_story.data
        if form.fd_input.data == "userstory":
            userstory = form.selected_user_story.data
            userstory += "\n"
            userstory += form.user_story_abstract.data
            inputdata.userstory = userstory
        if form.fd_input.data == "scopevision":
            inputdata.highlevelreq = form.scope_vision.data

        datatask = asyncio.to_thread(
            designdata.generate_functional_design,
            "data",
            inputdata
            )
        tasks.append(datatask)

    results = await asyncio.gather(*tasks)
    uidesign = ""
    servicesdesign = ""
    datadesign = ""

    result_index = 0
    if form.uifuncdesigncheck.data is True:
        uidesign = results[result_index]
        result_index += 1

    if form.servicesfuncdesigncheck.data is True:
        servicesdesign = results[result_index]
        result_index += 1

    if form.datafuncdesigncheck.data is True:
        datadesign = results[result_index]
        result_index += 1

    returndict = {
        "uidesign":uidesign,
        "servicesdesign":servicesdesign,
        "datadesign":datadesign
        }

    logger.info("Functional Design generation completed successfully")
    return returndict

async def generate_high_level_design(form: GenLiteMainForm):
    '''Orchestrates the generation of the High Level Design'''
    logger.info("Orchestrating the generation of the High Level Design")
    llmplatform = form.llm_platform_options.data

    tasks = []
    if form.uihlddesigncheck.data is True:
        designui = GenLiteDesign(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
        inputui = HighLevelDesignInput()

        if "applicationcontext" in form.fd_input_multi.data:
            inputui.applicationcontext = form.ecosystem_context.data
        if "businesscontext" in form.fd_input_multi.data:
            inputui.businesscontext = form.business_process_mapping.data
        if "processflow" in form.fd_input_multi.data:
            inputui.processflow = form.process_flow_mapping.data

        if form.fd_input.data == "epic":
            inputui.epic = form.epic_user_story.data
        if form.fd_input.data == "feature":
            inputui.feature = form.feature_user_story.data
        if form.fd_input.data == "userstory":
            userstory = form.selected_user_story.data
            userstory += "\n"
            userstory += form.user_story_abstract.data
            inputui.userstory = userstory
        if form.fd_input.data == "scopevision":
            inputui.highlevelreq = form.scope_vision.data

        inputui.functionaldesign = form.ui_functional_design.data

        uitask = asyncio.to_thread(
            designui.generate_high_level_design,
            "ui",
            inputui
            )
        tasks.append(uitask)

    if form.serviceshlddesigncheck.data is True:
        designservices = GenLiteDesign(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
        inputservices = HighLevelDesignInput()

        if "applicationcontext" in form.fd_input_multi.data:
            inputservices.applicationcontext = form.ecosystem_context.data
        if "businesscontext" in form.fd_input_multi.data:
            inputservices.businesscontext = form.business_process_mapping.data
        if "processflow" in form.fd_input_multi.data:
            inputservices.processflow = form.process_flow_mapping.data

        if form.fd_input.data == "epic":
            inputservices.epic = form.epic_user_story.data
        if form.fd_input.data == "feature":
            inputservices.feature = form.feature_user_story.data
        if form.fd_input.data == "userstory":
            userstory = form.selected_user_story.data
            userstory += "\n"
            userstory += form.user_story_abstract.data
            inputservices.userstory = userstory
        if form.fd_input.data == "scopevision":
            inputservices.highlevelreq = form.scope_vision.data

        inputservices.functionaldesign = form.services_functional_design.data

        servicestask = asyncio.to_thread(
            designservices.generate_high_level_design,
            "services",
            inputservices
            )
        tasks.append(servicestask)

    if form.datahlddesigncheck.data is True:
        designdata = GenLiteDesign(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
        inputdata = HighLevelDesignInput()

        if "applicationcontext" in form.fd_input_multi.data:
            inputdata.applicationcontext = form.ecosystem_context.data
        if "businesscontext" in form.fd_input_multi.data:
            inputdata.businesscontext = form.business_process_mapping.data
        if "processflow" in form.fd_input_multi.data:
            inputdata.processflow = form.process_flow_mapping.data

        if form.fd_input.data == "epic":
            inputdata.epic = form.epic_user_story.data
        if form.fd_input.data == "feature":
            inputdata.feature = form.feature_user_story.data
        if form.fd_input.data == "userstory":
            userstory = form.selected_user_story.data
            userstory += "\n"
            userstory += form.user_story_abstract.data
            inputdata.userstory = userstory
        if form.fd_input.data == "scopevision":
            inputdata.highlevelreq = form.scope_vision.data

        inputdata.functionaldesign = form.data_functional_design.data

        datatask = asyncio.to_thread(
            designdata.generate_high_level_design,
            "data",
            inputdata
            )
        tasks.append(datatask)

    results = await asyncio.gather(*tasks)
    uidesign = ""
    servicesdesign = ""
    datadesign = ""

    result_index = 0
    if form.uihlddesigncheck.data is True:
        uidesign = results[result_index]
        result_index += 1

    if form.serviceshlddesigncheck.data is True:
        servicesdesign = results[result_index]
        result_index += 1

    if form.datahlddesigncheck.data is True:
        datadesign = results[result_index]
        result_index += 1

    returndict = {
        "uidesign":uidesign,
        "servicesdesign":servicesdesign,
        "datadesign":datadesign
        }

    logger.info("High Level Design generation completed successfully")
    return returndict

async def generate_low_level_design(form: GenLiteMainForm):
    '''Orchestrates the generation of the Low Level Design'''
    logger.info("Orchestrating the generation of the Low Level Design")
    llmplatform = form.llm_platform_options.data

    tasks = []
    if form.uidddesigncheck.data is True:
        designui = GenLiteDesign(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
        inputui = LowLevelDesignInput()

        if "applicationcontext" in form.fd_input_multi.data:
            inputui.applicationcontext = form.ecosystem_context.data
        if "businesscontext" in form.fd_input_multi.data:
            inputui.businesscontext = form.business_process_mapping.data
        if "processflow" in form.fd_input_multi.data:
            inputui.processflow = form.process_flow_mapping.data

        if form.fd_input.data == "epic":
            inputui.epic = form.epic_user_story.data
        if form.fd_input.data == "feature":
            inputui.feature = form.feature_user_story.data
        if form.fd_input.data == "userstory":
            userstory = form.selected_user_story.data
            userstory += "\n"
            userstory += form.user_story_abstract.data
            inputui.userstory = userstory
        if form.fd_input.data == "scopevision":
            inputui.highlevelreq = form.scope_vision.data

        inputui.functionaldesign = form.ui_functional_design.data
        inputui.highleveldesign = form.ui_high_level_design.data

        uitask = asyncio.to_thread(
            designui.generate_low_level_design,
            "ui",
            inputui
            )
        tasks.append(uitask)

    if form.servicesdddesigncheck.data is True:
        designservices = GenLiteDesign(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
        inputservices = LowLevelDesignInput()

        if "applicationcontext" in form.fd_input_multi.data:
            inputservices.applicationcontext = form.ecosystem_context.data
        if "businesscontext" in form.fd_input_multi.data:
            inputservices.businesscontext = form.business_process_mapping.data
        if "processflow" in form.fd_input_multi.data:
            inputservices.processflow = form.process_flow_mapping.data

        if form.fd_input.data == "epic":
            inputservices.epic = form.epic_user_story.data
        if form.fd_input.data == "feature":
            inputservices.feature = form.feature_user_story.data
        if form.fd_input.data == "userstory":
            userstory = form.selected_user_story.data
            userstory += "\n"
            userstory += form.user_story_abstract.data
            inputservices.userstory = userstory
        if form.fd_input.data == "scopevision":
            inputservices.highlevelreq = form.scope_vision.data

        inputservices.functionaldesign = form.services_functional_design.data
        inputservices.highleveldesign = form.services_high_level_design.data

        servicestask = asyncio.to_thread(
            designservices.generate_low_level_design,
            "services",
            inputservices
            )
        tasks.append(servicestask)

    if form.datadddesigncheck.data is True:
        designdata = GenLiteDesign(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
        inputdata = LowLevelDesignInput()

        if "applicationcontext" in form.fd_input_multi.data:
            inputdata.applicationcontext = form.ecosystem_context.data
        if "businesscontext" in form.fd_input_multi.data:
            inputdata.businesscontext = form.business_process_mapping.data
        if "processflow" in form.fd_input_multi.data:
            inputdata.processflow = form.process_flow_mapping.data

        if form.fd_input.data == "epic":
            inputdata.epic = form.epic_user_story.data
        if form.fd_input.data == "feature":
            inputdata.feature = form.feature_user_story.data
        if form.fd_input.data == "userstory":
            userstory = form.selected_user_story.data
            userstory += "\n"
            userstory += form.user_story_abstract.data
            inputdata.userstory = userstory
        if form.fd_input.data == "scopevision":
            inputdata.highlevelreq = form.scope_vision.data

        inputdata.functionaldesign = form.data_functional_design.data
        inputdata.highleveldesign = form.data_high_level_design.data

        datatask = asyncio.to_thread(
            designdata.generate_low_level_design,
            "data",
            inputdata
            )
        tasks.append(datatask)

    results = await asyncio.gather(*tasks)
    uidesign = ""
    servicesdesign = ""
    datadesign = ""

    result_index = 0
    if form.uidddesigncheck.data is True:
        uidesign = results[result_index]
        result_index += 1

    if form.servicesdddesigncheck.data is True:
        servicesdesign = results[result_index]
        result_index += 1

    if form.datadddesigncheck.data is True:
        datadesign = results[result_index]
        result_index += 1

    returndict = {
        "uidesign":uidesign,
        "servicesdesign":servicesdesign,
        "datadesign":datadesign
        }

    logger.info("Low Level Design generation completed successfully")
    return returndict

async def generate_functional_design_from_image(filepath):
    '''Orchestrates the generation of the Functional Design from Image'''
    logger.info("Orchestrating the generation of the Functional Design from Image")

    designfromimage = GenLiteDesignFromImage(
        filepath,
        "azureopenai"
        )

    functional_design = await asyncio.to_thread(
        designfromimage.generate_functional_design
        )

    logger.info("Function Design from Image generation completed successfully")
    return functional_design
