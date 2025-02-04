'''Orchestrates the generation of the Feature'''
import asyncio
import logging
from appext.models.form import GenLiteMainForm
from plugins.codeservice.controller import GenLiteCode
from plugins.codeservice.model import (
    CodeInput
)

logger=logging.getLogger("GenLiteApp")

async def generate_code(form: GenLiteMainForm):
    '''Generate the Code'''
    logger.info("Generating Code")

    llmplatform = form.llm_platform_options.data

    uicode = ""
    servicecode = ""
    datacode = ""

    if form.uicodecheck.data is True:
        uiinput = CodeInput(
            applicationcontext=form.ecosystem_context.data,
            highleveldesign=form.ui_high_level_design.data,
            lowleveldesign=form.ui_detailed_design.data
        )
        uicodeobject = GenLiteCode(
            industry=form.industry.data,
            llmplatform=llmplatform
        )
        uilanguage = form.frontend_code_language.data
        uicode = await asyncio.to_thread(
            uicodeobject.generate,
            uiinput,
            "ui",
            uilanguage
            )
        logger.info("UI Code Generated")

    if form.servicescodecheck.data is True:
        serviceinput = CodeInput(
            applicationcontext=form.ecosystem_context.data,
            highleveldesign=form.services_high_level_design.data,
            lowleveldesign=form.services_detailed_design.data
        )
        servicecodeobject = GenLiteCode(
            industry=form.industry.data,
            llmplatform=llmplatform
        )
        servicelanguage = form.code_language.data
        servicecode = await asyncio.to_thread(
            servicecodeobject.generate,
            serviceinput,
            "services",
            servicelanguage
            )
        logger.info("Service Code Generated")

    if form.datacodecheck.data is True:
        datainput = CodeInput(
            applicationcontext=form.ecosystem_context.data,
            highleveldesign=form.data_high_level_design.data,
            lowleveldesign=form.data_detailed_design.data
        )
        datacodeobject = GenLiteCode(
            industry=form.industry.data,
            llmplatform=llmplatform
        )
        datalanguage = "sql"
        datacode = await asyncio.to_thread(
            datacodeobject.generate,
            datainput,
            "data",
            datalanguage
            )
        logger.info("Data Code Generated")

    returndict = {
        "uicode": uicode,
        "servicescode": servicecode,
        "datacode": datacode
    }
    logger.info("Code generation completed successfully")
    return returndict
