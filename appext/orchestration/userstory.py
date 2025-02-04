'''Orchestrates the generation of the Feature'''
import asyncio
import logging
from appext.models.form import GenLiteMainForm
from plugins.userstoryservice.controller import GenLiteUserStory
from plugins.userstoryservice.model import (
    UserStoryInput,
    ExpandUserStoryInput
    )

logger=logging.getLogger("GenLiteApp")

async def generate_userstory(form: GenLiteMainForm):
    '''Orchestrates the generation of the User Story'''
    logger.info("Orchestrating the generation of the User Story")
    llmplatform = form.llm_platform_options.data
    userstorygenerator = GenLiteUserStory(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
    userstorydictobject = UserStoryInput()
    userstoryinputmulti = form.userstories_input_multi.data

    if 'applicationcontext' in userstoryinputmulti:
        userstorydictobject.applicationcontext = form.ecosystem_context.data
    else:
        userstorydictobject.applicationcontext = ""
    if 'businesscontext' in userstoryinputmulti:
        userstorydictobject.businesscontext = form.business_process_mapping.data
    else:
        userstorydictobject.businesscontext = ""
    if 'processflow' in userstoryinputmulti:
        userstorydictobject.processflow = form.process_flow_mapping.data
    else:
        userstorydictobject.processflow = ""
    if 'scopevision' in userstoryinputmulti:
        userstorydictobject.highlevelreq = form.scope_vision.data
    else:
        userstorydictobject.highlevelreq = ""

    userstorydictobject.epic = form.epic_user_story.data
    userstorydictobject.feature = form.feature_user_story.data
    slicingmethod = form.slicingmethod.data

    userstory = await asyncio.to_thread(
        userstorygenerator.generate,
        slicingmethod,
        userstorydictobject
        )

    logger.info("User Story generation completed successfully")
    return userstory

async def expand_userstory(form: GenLiteMainForm):
    '''Orchestrates the expansion of the User Story'''
    logger.info("Orchestrating the expansion of the User Story")
    llmplatform = form.llm_platform_options.data
    userstorygenerator = GenLiteUserStory(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
    userstorydictobject = ExpandUserStoryInput()
    userstoryinputmulti = form.userstories_input_multi.data

    if 'applicationcontext' in userstoryinputmulti:
        userstorydictobject.applicationcontext = form.ecosystem_context.data
    else:
        userstorydictobject.applicationcontext = ""
    if 'businesscontext' in userstoryinputmulti:
        userstorydictobject.businesscontext = form.business_process_mapping.data
    else:
        userstorydictobject.businesscontext = ""
    if 'processflow' in userstoryinputmulti:
        userstorydictobject.processflow = form.process_flow_mapping.data
    else:
        userstorydictobject.processflow = ""
    if 'scopevision' in userstoryinputmulti:
        userstorydictobject.highlevelreq = form.scope_vision.data
    else:
        userstorydictobject.highlevelreq = ""

    userstorydictobject.epic = form.epic_user_story.data
    userstorydictobject.feature = form.feature_user_story.data
    userstorydictobject.userstory = form.selected_user_story.data

    userstory = await asyncio.to_thread(
        userstorygenerator.expand,
        userstorydictobject
        )
    
    logger.info("User Story expansion completed successfully")
    return userstory

async def generate_userstory_tasks(form: GenLiteMainForm):
    '''Orchestrates the generation of the User Story'''
    logger.info("Orchestrating the generation of the User Story - Tasks")
    llmplatform = form.llm_platform_options.data
    userstorygenerator = GenLiteUserStory(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
    userstorydictobject = ExpandUserStoryInput()
    userstoryinputmulti = form.userstories_input_multi.data

    if 'applicationcontext' in userstoryinputmulti:
        userstorydictobject.applicationcontext = form.ecosystem_context.data
    else:
        userstorydictobject.applicationcontext = ""
    if 'businesscontext' in userstoryinputmulti:
        userstorydictobject.businesscontext = form.business_process_mapping.data
    else:
        userstorydictobject.businesscontext = ""
    if 'processflow' in userstoryinputmulti:
        userstorydictobject.processflow = form.process_flow_mapping.data
    else:
        userstorydictobject.processflow = ""
    if 'scopevision' in userstoryinputmulti:
        userstorydictobject.highlevelreq = form.scope_vision.data
    else:
        userstorydictobject.highlevelreq = ""

    userstorydictobject.epic = form.epic_user_story.data
    userstorydictobject.feature = form.feature_user_story.data
    userstorydictobject.userstory = form.selected_user_story.data
    userstorydictobject.userstory += form.user_story_abstract.data

    userstory = await asyncio.to_thread(
        userstorygenerator.generate_tasks,
        userstorydictobject
        )
    
    logger.info("User Story - Tasks generation completed successfully")
    return userstory
