'''Orchestrates the generation of the Feature'''
import asyncio
import logging
from appext.models.form import GenLiteMainForm
from plugins.featureservice.controller import GenLiteFeature
from plugins.featureservice.model import (
    FeatureInput,
    ExpandFeatureInput
    )

logger=logging.getLogger("GenLiteApp")

async def generate_feature(form: GenLiteMainForm):
    '''Orchestrates the generation of the Feature'''
    logger.info("Orchestrating the generation of the Feature")
    llmplatform = form.llm_platform_options.data
    featuregenerator = GenLiteFeature(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
    featuredictobject = FeatureInput()
    featureinputmulti = form.features_input_multi.data

    if 'applicationcontext' in featureinputmulti:
        featuredictobject.applicationcontext = form.ecosystem_context.data
    else:
        featuredictobject.applicationcontext = ""
    if 'businesscontext' in featureinputmulti:
        featuredictobject.businesscontext = form.business_process_mapping.data
    else:
        featuredictobject.businesscontext = ""
    if 'processflow' in featureinputmulti:
        featuredictobject.processflow = form.process_flow_mapping.data
    else:
        featuredictobject.processflow = ""
    if 'scopevision' in featureinputmulti:
        featuredictobject.highlevelreq = form.scope_vision.data
    else:
        featuredictobject.highlevelreq = ""

    featuredictobject.epic = form.epic_user_story.data

    feature = await asyncio.to_thread(
        featuregenerator.generate,
        featuredictobject
        )

    logger.info("Feature generation completed successfully")
    return feature

async def expand_feature(form: GenLiteMainForm):
    '''Orchestrates the expansion of the Feature'''
    logger.info("Orchestrating the expansion of the Feature")
    llmplatform = form.llm_platform_options.data
    featuregenerator = GenLiteFeature(
        llmplatform=llmplatform,
        industry=form.industry.data
        )
    featuredictobject = ExpandFeatureInput()
    featureinputmulti = form.features_input_multi.data

    if 'applicationcontext' in featureinputmulti:
        featuredictobject.applicationcontext = form.ecosystem_context.data
    else:
        featuredictobject.applicationcontext = ""
    if 'businesscontext' in featureinputmulti:
        featuredictobject.businesscontext = form.business_process_mapping.data
    else:
        featuredictobject.businesscontext = ""
    if 'processflow' in featureinputmulti:
        featuredictobject.processflow = form.process_flow_mapping.data
    else:
        featuredictobject.processflow = ""
    if 'scopevision' in featureinputmulti:
        featuredictobject.highlevelreq = form.scope_vision.data
    else:
        featuredictobject.highlevelreq = ""

    featuredictobject.epic = form.epic_user_story.data
    featuredictobject.feature = form.selected_feature.data

    feature = await asyncio.to_thread(
        featuregenerator.expand,
        featuredictobject
        )

    logger.info("Feature expansion completed successfully")
    return feature
