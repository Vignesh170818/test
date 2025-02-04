'''This module orchestrates the generation, review and application of the review of the EPIC'''
import asyncio
import logging
from appext.models.form import GenLiteMainForm
from plugins.epicservice.controller import GenLiteEPIC
from plugins.epicservice.model import (
    EPICInput,
    EPICReviewInput,
    EPICApplyReviewInput
    )
logger=logging.getLogger("GenLiteApp")

async def generate_epic(form: GenLiteMainForm):
    '''Orchestrates the generation of the EPIC'''
    logger.info("Orchestrating the generation of the EPIC")
    llmplatform = form.llm_platform_options.data
    epicgenerator = GenLiteEPIC(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
    epicdictobject = EPICInput()
    epicinputmulti = form.epic_input_multi.data

    if 'applicationcontext' in epicinputmulti:
        epicdictobject.applicationcontext = form.ecosystem_context.data
    else:
        epicdictobject.applicationcontext = ""
    if 'businesscontext' in epicinputmulti:
        epicdictobject.businesscontext = form.business_process_mapping.data
    else:
        epicdictobject.businesscontext = ""
    if 'processflow' in epicinputmulti:
        epicdictobject.processflow = form.process_flow_mapping.data
    else:
        epicdictobject.processflow = ""
    if 'scopevision' in epicinputmulti:
        epicdictobject.highlevelreq = form.scope_vision.data
    else:
        epicdictobject.highlevelreq = ""
        
    epic = await asyncio.to_thread(
        epicgenerator.generate,
        epicdictobject,
        form
        )

    return epic

async def review_epic(form: GenLiteMainForm):
    '''Orchestrates the review of the EPIC'''
    logger.info("Orchestrating the review of the EPIC")
    llmplatform = form.llm_platform_options.data
    epicgenerator = GenLiteEPIC(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
    epicdictobject = EPICReviewInput()
    epicinputmulti = form.epic_input_multi.data

    if 'applicationcontext' in epicinputmulti:
        epicdictobject.applicationcontext = form.ecosystem_context.data
    else:
        epicdictobject.applicationcontext = ""
    if 'businesscontext' in epicinputmulti:
        epicdictobject.businesscontext = form.business_process_mapping.data
    else:
        epicdictobject.businesscontext = ""
    if 'processflow' in epicinputmulti:
        epicdictobject.processflow = form.process_flow_mapping.data
    else:
        epicdictobject.processflow = ""
    if 'scopevision' in epicinputmulti:
        epicdictobject.highlevelreq = form.scope_vision.data
    else:
        epicdictobject.highlevelreq = ""

    epicdictobject.epic = form.epic_user_story.data

    reviewcomments = await asyncio.to_thread(
        epicgenerator.review,
        epicdictobject
        )

    return reviewcomments

async def apply_review_epic(form: GenLiteMainForm):
    '''Orchestrates the application of the review of the EPIC'''
    logger.info("Orchestrating the application of the review of the EPIC")
    llmplatform = form.llm_platform_options.data
    print(f"llmplatform: {llmplatform}")
    epicgenerator = GenLiteEPIC(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
    epicdictobject = EPICApplyReviewInput()
    epicinputmulti = form.epic_input_multi.data

    if 'applicationcontext' in epicinputmulti:
        epicdictobject.applicationcontext = form.ecosystem_context.data
    else:
        epicdictobject.applicationcontext = ""
    if 'businesscontext' in epicinputmulti:
        epicdictobject.businesscontext = form.business_process_mapping.data
    else:
        epicdictobject.businesscontext = ""
    if 'processflow' in epicinputmulti:
        epicdictobject.processflow = form.process_flow_mapping.data
    else:
        epicdictobject.processflow = ""
    if 'scopevision' in epicinputmulti:
        epicdictobject.highlevelreq = form.scope_vision.data
    else:
        epicdictobject.highlevelreq = ""

    epicdictobject.epic = form.epic_user_story.data
    epicdictobject.reviewcomments = form.epic_review_comments.data

    modifiedepic = await asyncio.to_thread(
        epicgenerator.applyreview,
        epicdictobject
        )

    return modifiedepic
