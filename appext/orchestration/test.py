'''Orchestrates the generation of the Feature'''
import asyncio
from appext.models.form import GenLiteMainForm
from plugins.testservice.controller import GenLiteTest
from plugins.testservice.model import (
    TestScenariosInput,
    TestCasesInput,
    TestScriptsInput,
    ToolTestScriptsInput
    )
import logging

logger=logging.getLogger("GenLiteApp")

async def generate_test_scenarios(
        form: GenLiteMainForm
        ):
    '''Generates test scenarios'''
    logger.info("Orchestrating the generation of Test Scenarios")
    inputobj = TestScenariosInput()

    stmulti = form.st_input_multi.data

    if "applicationcontext" in stmulti:
        inputobj.applicationcontext = form.ecosystem_context.data
    if "businesscontext" in stmulti:
        inputobj.businesscontext = form.business_process_mapping.data
    if "processflow" in stmulti:
        inputobj.processflow = form.process_flow_mapping.data
    if "scopevision" in stmulti:
        inputobj.highlevelreq = form.scope_vision.data

    if form.st_key_input.data == "epic":
        inputobj.epic = form.epic_user_story.data
    if form.st_key_input.data == "feature":
        inputobj.feature = form.feature_user_story.data
    if form.st_key_input.data == "userstory":
        userstory = form.selected_user_story.data
        userstory += "\n"
        userstory += form.user_story_abstract.data
        inputobj.userstory = userstory
    if form.st_key_input.data == "functional-ui":
        inputobj.functionaldesignui = form.ui_functional_design.data
    if form.st_key_input.data == "functional-services":
        inputobj.functionaldesignservices = form.services_functional_design.data
    if form.st_key_input.data == "functional-data":
        inputobj.functionaldesigndata = form.data_functional_design.data

    gentest = GenLiteTest(
        llmplatform=form.llm_platform_options.data,
        industry=form.industry.data
        )

    testscenarios = await asyncio.to_thread(
        gentest.generate_test_scenarios,
        inputobj
        )

    logger.info("Test Scenarios generation completed successfully")
    return testscenarios

async def generate_test_cases(
        form: GenLiteMainForm
        ):
    '''Generates test cases'''
    logger.info("Orchestrating the generation of the Test Cases")
    inputobj = TestCasesInput()

    stmulti = form.st_input_multi.data

    if "applicationcontext" in stmulti:
        inputobj.applicationcontext = form.ecosystem_context.data
    if "businesscontext" in stmulti:
        inputobj.businesscontext = form.business_process_mapping.data
    if "processflow" in stmulti:
        inputobj.processflow = form.process_flow_mapping.data
    if "scopevision" in stmulti:
        inputobj.highlevelreq = form.scope_vision.data

    if form.st_key_input.data == "epic":
        inputobj.epic = form.epic_user_story.data
    if form.st_key_input.data == "feature":
        inputobj.feature = form.feature_user_story.data
    if form.st_key_input.data == "userstory":
        userstory = form.selected_user_story.data
        userstory += "\n"
        userstory += form.user_story_abstract.data
        inputobj.userstory = userstory
    if form.st_key_input.data == "functional-ui":
        inputobj.functionaldesignui = form.ui_functional_design.data
    if form.st_key_input.data == "functional-services":
        inputobj.functionaldesignservices = form.services_functional_design.data
    if form.st_key_input.data == "functional-data":
        inputobj.functionaldesigndata = form.data_functional_design.data
    inputobj.testscenario = form.test_cases.data

    gentest = GenLiteTest(
        llmplatform=form.llm_platform_options.data,
        industry=form.industry.data
        )
    testcases = await asyncio.to_thread(
        gentest.generate_test_cases,
        inputobj
        )

    logger.info("Test Cases generation completed successfully")
    return testcases

async def generate_test_scripts(
        form: GenLiteMainForm
        ):
    '''Generates test scripts'''
    logger.info("Orchestrating the generation of the Test Scripts")
    inputobj = TestScriptsInput()

    stmulti = form.st_input_multi.data

    if "applicationcontext" in stmulti:
        inputobj.applicationcontext = form.ecosystem_context.data
    if "businesscontext" in stmulti:
        inputobj.businesscontext = form.business_process_mapping.data
    if "processflow" in stmulti:
        inputobj.processflow = form.process_flow_mapping.data
    if "scopevision" in stmulti:
        inputobj.highlevelreq = form.scope_vision.data

    if form.st_key_input.data == "epic":
        inputobj.epic = form.epic_user_story.data
    if form.st_key_input.data == "feature":
        inputobj.feature = form.feature_user_story.data
    if form.st_key_input.data == "userstory":
        userstory = form.selected_user_story.data
        userstory += "\n"
        userstory += form.user_story_abstract.data
        inputobj.userstory = userstory
    if form.st_key_input.data == "functional-ui":
        inputobj.functionaldesignui = form.ui_functional_design.data
    if form.st_key_input.data == "functional-services":
        inputobj.functionaldesignservices = form.services_functional_design.data
    if form.st_key_input.data == "functional-data":
        inputobj.functionaldesigndata = form.data_functional_design.data
    inputobj.testscenario = form.test_plan.data
    inputobj.testcase = form.test_cases.data

    gentest = GenLiteTest(
        llmplatform=form.llm_platform_options.data,
        industry=form.industry.data
        )
    testscripts = await asyncio.to_thread(gentest.generate_test_scripts, inputobj)

    logger.info("Test Scripts generation completed successfully")
    return testscripts

async def generate_tool_test_scripts(
        form: GenLiteMainForm
        ):
    '''Generates tool test scripts'''
    logger.info("Orchestrating the generation of the Tool Test Scripts")
    inputobj = ToolTestScriptsInput()

    stmulti = form.st_input_multi.data

    if "applicationcontext" in stmulti:
        inputobj.applicationcontext = form.ecosystem_context.data
    if "businesscontext" in stmulti:
        inputobj.businesscontext = form.business_process_mapping.data
    if "processflow" in stmulti:
        inputobj.processflow = form.process_flow_mapping.data
    if "scopevision" in stmulti:
        inputobj.highlevelreq = form.scope_vision.data

    if form.st_key_input.data == "epic":
        inputobj.epic = form.epic_user_story.data
    if form.st_key_input.data == "feature":
        inputobj.feature = form.feature_user_story.data
    if form.st_key_input.data == "userstory":
        userstory = form.selected_user_story.data
        userstory += "\n"
        userstory += form.user_story_abstract.data
        inputobj.userstory = userstory
    if form.st_key_input.data == "functional-ui":
        inputobj.functionaldesignui = form.ui_functional_design.data
    if form.st_key_input.data == "functional-services":
        inputobj.functionaldesignservices = form.services_functional_design.data
    if form.st_key_input.data == "functional-data":
        inputobj.functionaldesigndata = form.data_functional_design.data
    inputobj.testscenario = form.test_plan.data
    inputobj.testcase = form.test_cases.data
    inputobj.testscript = form.test_scripts.data

    gentest = GenLiteTest(
        llmplatform=form.llm_platform_options.data,
        industry=form.industry.data
        )
    testscripts = await asyncio.to_thread(gentest.generate_tool_test_scripts, inputobj)

    logger.info("Tool Test Scripts generation completed successfully")
    return testscripts

async def generate_test_scripts_tool(
        form: GenLiteMainForm
        ):
    '''Generates test scripts tool'''
    logger.info("Orchestrating the generation of the Test Script Tool")
    inputobj = ToolTestScriptsInput()

    stmulti = form.st_input_multi.data

    if "applicationcontext" in stmulti:
        inputobj.applicationcontext = form.ecosystem_context.data
    if "businesscontext" in stmulti:
        inputobj.businesscontext = form.business_process_mapping.data
    if "processflow" in stmulti:
        inputobj.processflow = form.process_flow_mapping.data
    if "scopevision" in stmulti:
        inputobj.highlevelreq = form.scope_vision.data

    if form.st_key_input.data == "epic":
        inputobj.epic = form.epic_user_story.data
    if form.st_key_input.data == "feature":
        inputobj.feature = form.feature_user_story.data
    if form.st_key_input.data == "userstory":
        userstory = form.selected_user_story.data
        userstory += "\n"
        userstory += form.user_story_abstract.data
        inputobj.userstory = userstory
    if form.st_key_input.data == "functional-ui":
        inputobj.functionaldesignui = form.ui_functional_design.data
    if form.st_key_input.data == "functional-services":
        inputobj.functionaldesignservices = form.services_functional_design.data
    if form.st_key_input.data == "functional-data":
        inputobj.functionaldesigndata = form.data_functional_design.data
    inputobj.testscenario = form.test_plan.data
    inputobj.testcase = form.test_cases.data
    inputobj.testscript = form.test_scripts.data
    inputobj.tool = form.system_test_tool.data

    gentest = GenLiteTest(
        llmplatform=form.llm_platform_options.data,
        industry=form.industry.data
        )
    testscripts = await asyncio.to_thread(gentest.generate_tool_test_scripts, inputobj)

    logger.info("Test Script Tool generation completed successfully")
    return testscripts
