'''This module orchestrates the generation, review and application of the review of the EPIC'''
import logging
from appext.models.form import GenLiteMainForm
from plugins.deploymentservice.controller import GenLiteDeployment
from plugins.deploymentservice.model import DeploymentInput

logger=logging.getLogger("GenLiteApp")

async def generate_deployment(form: GenLiteMainForm):
    '''Orchestrates the generation of the EPIC'''
    logger.info("Orchestrating the generation of the Deployment")
    llmplatform = form.llm_platform_options.data

    uideploymentscript = ""
    servicesdeploymentscript = ""
    datadeploymentscript = ""

    if form.uideploymentcheck.data is True:
        object_ui = GenLiteDeployment(
        llmplatform=llmplatform
        )
        input_ui = DeploymentInput()
        input_ui.architecture = form.architecture_ui.data
        input_ui.design = form.ui_detailed_design.data
        platform = form.platform_choice.data
        uideploymentscript = object_ui.deployment_generate(
            input_ui,
            platform
            )

    if form.servicesdeploymentcheck.data is True:
        object_services = GenLiteDeployment(
        llmplatform=llmplatform
        )
        input_services = DeploymentInput()
        input_services.architecture = form.architecture_services.data
        input_services.design = form.services_detailed_design.data
        platform = form.platform_choice.data
        servicesdeploymentscript = object_services.deployment_generate(
            input_services,
            platform
            )

    if form.datadeploymentcheck.data is True:
        object_data = GenLiteDeployment(
        llmplatform=llmplatform
        )
        input_data = DeploymentInput()
        input_data.architecture = form.architecture_data.data
        input_data.design = form.data_detailed_design.data
        platform = form.platform_choice.data
        datadeploymentscript = object_data.deployment_generate(
            input_data,
            platform
            )

    returndict = {
        "uideployment": uideploymentscript,
        "servicesdeployment": servicesdeploymentscript,
        "datadeployment": datadeploymentscript
        }

    logger.info("Deployment generation completed successfully")
    return returndict
