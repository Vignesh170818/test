'''This module contains the GenLiteForm class which is used to create the'''
from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    BooleanField,
    TextAreaField,
    SelectField,
    SelectMultipleField,
    HiddenField,
    StringField
    )
from wtforms.validators import Length
from genliteappext.genliteapp import GenLiteAppExtension

class GenLiteMainForm(FlaskForm):
    '''Main Form'''
    llm_platform_options = SelectField('Model', choices=[
        ('azureopenai', 'GPT 3.5'),
        ('azureopenaigpt4', 'GPT 4'),
        ('geminipro', 'Gemini Pro'),
        ('textbison', 'Bison')
        # ('awstitan', 'Titan')
        ],
        default=['azureopenai']
        )

    '''Industry Form'''

    # inputTab related fields
    industry = GenLiteAppExtension().load_industry()
    ecosystem_context = TextAreaField(
        'Ecosystem Context',
        validators=[Length(max=15000)]
        )
    scope_vision = TextAreaField('Scope / Vision / HLR',validators=[Length(max=15000)])
    industry_submit_button = SubmitField('Get Ecosystem Context')

    move_to_business_context_button = SubmitField('Next: Generate Business Context')

    #businessContextTab related fields
    get_business_context_button = SubmitField('Get Business Context')
    business_process_mapping = TextAreaField(
        'Business Process Mapping (Vector Mapped)',
        validators=[Length(max=15000)]
        )
    process_flow_mapping = TextAreaField(
        'Process Flow Mapping (AI Generated)',
        validators=[Length(max=15000)]
        )
    treeviewindustry = GenLiteAppExtension().load_industry()

    move_to_epic_button = SubmitField('Next: Generate EPIC')

    #businessCaseTab related fields
    business_case_input = SelectField('Input for Business Case', choices=[
        ('epic', 'EPIC User Story'),
        ('feature', 'Feature User Story'),
        ('userstory', 'Selected User Story')
        ],
        default='userstory'
        )
    generate_business_case_button = SubmitField('Generate Business Case')
    business_case = TextAreaField('Business Case',validators=[Length(max=15000)])

    #epicTab related fields
    generate_epic_button = SubmitField('Generate EPIC')
    epic_review_comments = TextAreaField('Review Comments',validators=[Length(max=15000)])
    epic_persona_type = SelectField('Persona Type', choices=[
        ('dummy', 'Select Persona Type'),
        ('technical', 'Tech Oriented'),
        ('process', 'Process Oriented'),
        ('business', 'Business Oriented'),
        ('customer', 'Customer Oriented')
        ]
        )
    
    epic_external_id = StringField('EPIC External Id',validators=[Length(max=15)])
    get_epic_details = SubmitField('Get Epic Details')
    reset_epic_details = SubmitField('Reset Epic Details')
    gen_epic_review_button = SubmitField('Generate Review Comments')
    apply_epic_review_button = SubmitField('Apply Review Comments')

    epic_input_multi = SelectMultipleField('Inputs for EPIC', choices=[
        ('applicationcontext', 'Application Context'),
        ('businesscontext', 'Business Context'),
        ('processflow', 'Process Flow'),
        ('scopevision', 'Scope / Vision / HLR')
        ],
        default=['applicationcontext', 'businesscontext', 'scopevision']
        )
    epic_user_story = TextAreaField('Abstract',validators=[Length(max=15000)])
    epicInputFlushCollapseOne = SelectMultipleField('', choices=[])

    #featuresTab related fields
    generate_feature_button = SubmitField('Next: Generate Features')
    expand_feature_button = SubmitField('Expand Feature')

    features_input_multi = SelectMultipleField('Inputs for Features', choices=[
        ('applicationcontext', 'Application Context'),
        ('businesscontext', 'Business Context'),
        ('processflow', 'Process Flow'),
        ('scopevision', 'Scope / Vision / HLR'),
        ('epic', 'EPIC User Story')
        ],
        default=['applicationcontext', 'businesscontext', 'epic']
        )
    
    feature_external_id = StringField('Feature External Id',validators=[Length(max=15)])
    get_feature_details = SubmitField('Get Feature Details')
    reset_feature_details = SubmitField('Reset Feature Details')
    features_list = TextAreaField('Features List',validators=[Length(max=15000)])
    selected_feature = TextAreaField('Selected Feature',validators=[Length(max=15000)])
    feature_user_story = TextAreaField('Feature Abstract',validators=[Length(max=15000)])

    #userStoriesTab related fields

    userstories_input_multi = SelectMultipleField(
        'Inputs for User Stories',
        choices=[
        ('applicationcontext', 'Application Context'),
        ('businesscontext', 'Business Context'),
        ('processflow', 'Process Flow'),
        ('scopevision', 'Scope / Vision / HLR'),
        ('epic', 'EPIC User Story'),
        ('feature', 'Feature User Story')
        ],
        default=['applicationcontext', 'businesscontext', 'epic', 'feature']
        )

    slicingmethod = SelectField('Slicing Method', choices=[
        ('dummy', 'Select Slicing Method'),
        ('functionalslicing', 'Functional Slicing'),
        ('verticalslicing', 'Vertical Slicing'),
        ('uislicing', 'User Interface Slicing'),
        ('dataslicing', 'Data-Driven Slicing'),
        ('securityslicing', 'Compliance and Security Slicing'),
        ('testdrivenslicing', 'Test-Driven Slicing')
        ],
        default='verticalslicing'
        )
    generate_user_stories_button = SubmitField('Generate User Stories')
    user_story_external_id = StringField('User Story External Id',validators=[Length(max=15)])
    get_user_story_details = SubmitField('Get User Story Details')
    reset_user_story_details = SubmitField('Reset User Story Details')
    expand_user_story_button = SubmitField('Expand User Story')
    consolidate_workitems_button = SubmitField('Consolidate Workitems')
    push_to_alm_button = SubmitField('Push to ALM')
    show_download = SubmitField('Download JSON')
    # download_json_atag = HiddenField("Download JSON File Name")
    merge_status_button = SubmitField('Check Status')
    user_stories_list = TextAreaField('User Stories',validators=[Length(max=15000)])
    selected_user_story = TextAreaField('Selected User Story',validators=[Length(max=15000)])
    user_story_abstract = TextAreaField('User Story Abstract',validators=[Length(max=15000)])
    entity_type = HiddenField('Entity Type')
    user_request_id = StringField("Registered User Request ID")
    status_response= TextAreaField("User Request Status")
    userstories_json = HiddenField('User Stories JSON')
    download_tool_queue = SubmitField('Download JSON')

    #functionalDesignTab related fields
    select_func_design_type = SelectMultipleField('Type of Design', choices=[
        ('ui', 'UI'),
        ('services', 'Services'),
        ('data', 'Data')
        ]
        )

    fd_input = SelectField('Input', choices=[
        ('dummy', 'Select Input'),
        ('epic', 'EPIC User Story'),
        ('feature', 'Feature User Story'),
        ('userstory', 'Selected User Story'),
        ('scopevision', 'Scope / Vision / HLR')
        ],
        default='userstory'
        )

    fd_input_multi = SelectMultipleField('Additional Inputs', choices=[
        ('applicationcontext', 'Application Context'),
        ('businesscontext', 'Business Context'),
        ('processflow', 'Process Flow')
        ],
        default=['applicationcontext', 'businesscontext']
        )

    fd_input_multi_checked = {
        "applicationcontext": True,
        "businesscontext": True,
        "processflow": False
    }

    fd_types = SelectMultipleField('Generate Types of Functional Design', choices=[
        ('ui_fd_design', 'UI Functional Design'),
        ('services_fd_design', 'Services Functional Design'),
        ('data_fd_design', 'Data Functional Design')
        ]
        )

    uifuncdesigncheck = BooleanField('UI Functional Design', default=True)
    servicesfuncdesigncheck = BooleanField('Services Functional Design', default=True)
    datafuncdesigncheck = BooleanField('Data Functional Design', default=True)

    generate_functional_design_button = SubmitField('Generate Functional Design')
    functional_design = TextAreaField("Functional Design",validators=[Length(max=15000)])

    fd_type_options = {
        "ui_fd_design": False,
        "services_fd_design": False,
        "data_fd_design": False
    }

    # generate_functional_design_button

    generate_ui_functional_design_button = SubmitField('Generate UI Functional Design')
    ui_functional_design = TextAreaField("UI Functional Design",validators=[Length(max=15000)])

    generate_services_functional_design_button = SubmitField('Generate Services Functional Design')
    services_functional_design = TextAreaField(
        "Services Functional Design",
        validators=[Length(max=15000)]
        )

    generate_data_functional_design_button = SubmitField('Generate Data Functional Design')
    data_functional_design = TextAreaField("Data Functional Design",validators=[Length(max=15000)])

    #Download Button for FDD,HLD and DLD
    download_functional_design_button = SubmitField('Download Functional Design')
    download_fdd_filename = HiddenField("FDD File Name")
    download_highlevel_design_button = SubmitField('Download High Level Design')
    download_hld_filename = HiddenField("HLD File Name")
    download_detailed_design_button = SubmitField('Download Detailed Design')
    download_dld_filename = HiddenField("DLD File Name")

    #Functional Design from Image related fields
    fd_from_image = TextAreaField('Functional Design',validators=[Length(max=15000)])

    #highLevelDesignTab related fields
    generate_high_level_design_button = SubmitField('Generate High Level Design')
    high_level_design = TextAreaField(
        'High Level Design',
        validators=[Length(max=15000)]
        )

    hld_types = SelectMultipleField('Generate Types of High Level Design', choices=[
        ('ui_hld_design', 'UI High Level Design'),
        ('services_hld_design', 'Services High Level Design'),
        ('data_hld_design', 'Data High Level Design')
        ]
        )

    uihlddesigncheck = BooleanField('UI High Level Design', default=True)
    serviceshlddesigncheck = BooleanField('Services High Level Design', default=True)
    datahlddesigncheck = BooleanField('Data High Level Design', default=True)

    hld_type_options = {
        "ui_hld_design": False,
        "services_hld_design": False,
        "data_hld_design": False
    }

    generate_ui_high_level_design_button = SubmitField('Generate UI High Level Design')
    ui_high_level_design = TextAreaField("UI High Level Design",validators=[Length(max=15000)])

    generate_services_high_level_design_button = SubmitField('Generate Services High Level Design')
    services_high_level_design = TextAreaField(
        "Services High Level Design",
        validators=[Length(max=15000)]
        )

    generate_data_high_level_design_button = SubmitField('Generate Data High Level Design')
    data_high_level_design = TextAreaField("Data High Level Design",validators=[Length(max=15000)])

    #lowLevelDesignTab related fields
    generate_detailed_design_button = SubmitField('Generate Detailed Design')
    detailed_design = TextAreaField(
        'Detailed Design',
        validators=[Length(max=15000)]
        )

    dd_types = SelectMultipleField('Generate Types of Low Level Design', choices=[
        ('ui_dd_design', 'UI Low Level Design'),
        ('services_dd_design', 'Services Low Level Design'),
        ('data_dd_design', 'Data Low Level Design')
        ]
        )

    uidddesigncheck = BooleanField('UI Low Level Design', default=True)
    servicesdddesigncheck = BooleanField('Services Low Level Design', default=True)
    datadddesigncheck = BooleanField('Data Low Level Design', default=True)

    dd_type_options = {
        "ui_dd_design": False,
        "services_dd_design": False,
        "data_dd_design": False
    }

    generate_ui_detailed_design_button = SubmitField('Generate UI Detailed Design')
    ui_detailed_design = TextAreaField("UI Detailed Design",validators=[Length(max=15000)])

    generate_services_detailed_design_button = SubmitField('Generate Services Detailed Design')
    services_detailed_design = TextAreaField(
        "Services Detailed Design",
        validators=[Length(max=15000)]
        )

    generate_data_detailed_design_button = SubmitField('Generate Data Detailed Design')
    data_detailed_design = TextAreaField("Data Detailed Design",validators=[Length(max=15000)])

    #codeTab related fields
    generate_code_button = SubmitField('Generate Code')
    code_language = SelectField('Service Code Language', choices=[
        ('dummy', 'Select Language'),
        ('python', 'Python'),
        ('csharp', 'C#'),
        ('java', 'Java'),
        # ('springjava', 'Spring Java'),
        ('nodejs', 'Node JS'),
        # ('groovy', 'Groovy'),
        # ('kotlin', 'Kotlin'),
        ('azurefunctionjava', 'Azure Function Java'),
        ('azurefunctionpython', 'Azure Function Python'),
        # ('azurefunctionnodejs', 'Azure Function Node JS'),
        # ('azurefunctioncsharp', 'Azure Function C#'),
        ('googlefunctionpython', 'Google Function Python'),
        # ('googlefunctionnodejs', 'Google Function Node JS'),
        ('googlefunctionjava', 'Google Function Java'),
        # ('googlefunctioncsharp', 'Google Function C#'),
        ('awslambdapython', 'AWS Function Python'),
        # ('awsfunctionnodejs', 'AWS Function Node JS'),
        ('awslambdajava', 'AWS Function Java')
        # ('awsfunctioncsharp', 'AWS Function C#')
        ]
        )

    frontend_code_language = SelectField('UI Code Language', choices=[
        ('dummy', 'Select Language'),
        ('html', 'HTML'),
        ('angular', 'Angular'),
        ('react', 'React JS'),
        ('vue', 'Vue JS')
        ]
        )

    code_types = SelectMultipleField('Generate Types of Code', choices=[
        ('ui_code', 'UI Code'),
        ('services_code', 'Services Code'),
        ('data_code', 'Data Code')
        ]
        )

    code_type_options = {
        "ui_code": False,
        "services_code": False,
        "data_code": False
    }

    uicodecheck = BooleanField('UI Code', default=True)
    servicescodecheck = BooleanField('Services Code', default=True)
    datacodecheck = BooleanField('Data Code', default=True)

    generate_ui_code_button = SubmitField('Generate UI Code')
    ui_code = TextAreaField("UI Code",validators=[Length(max=15000)])

    generate_services_code_button = SubmitField('Generate Services Code')
    services_code = TextAreaField("Services Code",validators=[Length(max=15000)])

    generate_data_code_button = SubmitField('Generate Data Code')
    data_code = TextAreaField("Data Code",validators=[Length(max=15000)])
    
    generate_code_graph_button = SubmitField('Generate Code Graph')
    data_code_graph = TextAreaField("Code Graph",validators=[Length(max=15000)])


    #unitTestingTab related fields
    unit_test_tool = SelectField('Test Tool', choices=[
        ('dummy', 'Select Test Tool'),
        ('selenium', 'Selenium'),
        ('cucumber', 'Cucumber'),
        ('junit', 'JUnit'),
        ('pytest', 'PyTest'),
        ('mocha', 'Mocha')
        ]
        )
    #unit_testing = HiddenField('Unit Testing')

    generate_unit_testing_button = SubmitField('Generate Unit Testing')
    unit_testing=TextAreaField("Unit Testing",validators=[Length(max=15000)])

    #systemTestingTab related fields
    st_key_input = SelectField('Primary Input', choices=[
        ('dummy', 'Select Key Input'),
        ('epic', 'EPIC User Story'),
        ('feature', 'Feature User Story'),
        ('userstory', 'Selected User Story'),
        ('functional-ui', 'UI Functional Design'),
        ('functional-services', 'Services Functional Design'),
        ('functional-data', 'Data Functional Design')
        ],
        default='functional'
        )
    st_input_multi = SelectMultipleField('Additional Context', choices=[
        ('applicationcontext', 'Application Context'),
        ('businesscontext', 'Business Context'),
        ('processflow', 'Process Flow'),
        ('scopevision', 'Scope / Vision / HLR')
        ],
        default=['applicationcontext', 'businesscontext', 'scopevision']
        )

    generate_test_plan_button = SubmitField('Generate Test Plan')
    generate_test_cases_button = SubmitField('Generate Test Cases')
    generate_test_scripts_button = SubmitField('Generate Test Scripts')
    generate_tool_test_scripts_button = SubmitField('Generate Scripts')

    test_plan = TextAreaField('Test Plan',validators=[Length(max=15000)])
    test_cases = TextAreaField('Test Cases',validators=[Length(max=15000)])
    test_scripts = TextAreaField('Test Scripts',validators=[Length(max=15000)])

    system_test_tool = SelectField('Test Tool', choices=[
        ('dummy', 'Select Test Tool'),
        ('selenium', 'Selenium'),
        ('puppeteer', 'Puppeteer'),
        ('cypress', 'Cypress'),
        ('cucumber', 'Cucumber'),
        ('playwright', 'Playwright')
        ]
        )
    system_testing = HiddenField('System Testing')

    tool_test_script = TextAreaField('Test Scripts for Tool',validators=[Length(max=15000)])

    #archTab related fields
    generate_architecture_button = SubmitField('Generate Architecture')
    platform_choice = SelectField('Platform Choice', choices=[
        ('dummy', 'Select Platform'),
        ('azure', 'Azure'),
        ('aws', 'AWS'),
        ('gcp', 'GCP')
        ]
        )

    arch_types = SelectMultipleField('Generate Types of Architecture', choices=[
        ('ui_arch', 'UI Architecture'),
        ('services_arch', 'Services Architecture'),
        ('data_arch', 'Data Architecture')
        ]
        )

    arch_type_options = {
        "ui_arch": False,
        "services_arch": False,
        "data_arch": False
    }

    uiarchcheck = BooleanField('UI Architecture', default=True)
    servicesarchcheck = BooleanField('Services Architecture', default=True)
    dataarchcheck = BooleanField('Data Architecture', default=True)

    generate_ui_architecture_button = SubmitField('Generate UI Architecture')
    architecture_ui = TextAreaField("Architecture - UI",validators=[Length(max=15000)])

    generate_services_architecture_button = SubmitField('Generate Services Architecture')
    architecture_services = TextAreaField("Architecture - Services",validators=[Length(max=15000)])

    generate_data_architecture_button = SubmitField('Generate Data Architecture')
    architecture_data = TextAreaField("Architecture - Data",validators=[Length(max=15000)])

    #deploymentTab related fields
    deployment_types = SelectMultipleField('Generate Types of Deployment Scripts', choices=[
        ('ui_deployment', 'UI Deployment Scripts'),
        ('services_deployment', 'Services Deployment Scripts'),
        ('data_deployment', 'Data Deployment Scripts')
        ]
        )

    deployment_type_options = {
        "ui_deployment": False,
        "services_deployment": False,
        "data_deployment": False
    }

    uideploymentcheck = BooleanField('UI Deployment Scripts', default=True)
    servicesdeploymentcheck = BooleanField('Services Deployment Scripts', default=True)
    datadeploymentcheck = BooleanField('Data Deployment Scripts', default=True)

    generate_deployment_button = SubmitField('Generate Deployment Scripts')

    generate_deployment_ui_button = SubmitField('Generate Deployment Scripts - UI')
    deployment_strategy_ui = TextAreaField(
        'Deployment Strategy - UI',
        validators=[Length(max=15000)]
        )

    generate_deployment_services_button = SubmitField('Generate Deployment Scripts - Services')
    deployment_strategy_services = TextAreaField(
        'Deployment Strategy - Services',
        validators=[Length(max=15000)]
        )

    generate_deployment_data_button = SubmitField('Generate Deployment Scripts - Data')
    deployment_strategy_data = TextAreaField(
        'Deployment Strategy - Data',
        validators=[Length(max=15000)]
        )

    #treeViewTab related fields
    treeview_content = HiddenField('Treeview Content')
    popovercontent = HiddenField('Popover Content')

    #componentDiagramTab related fields
    generate_component_diagram_button = SubmitField('Generate')
    component_diagram = TextAreaField('Component Diagram')

    #code map related fields
    fdsearchtextarea = HiddenField(
        'Requirements / Functional Design'
        )

    code_search_input = SelectField('Code Search Input', choices=[
        ('dummy', 'Select Code Search Input'),
        ('scopevision', 'Scope / Vision / HLR'),
        ('epic', 'EPIC User Story'),
        ('feature', 'Feature User Story'),
        ('userstory', 'Selected User Story'),
        ('functional-ui', 'UI Functional Design'),
        ('functional-services', 'Services Functional Design'),
        ('functional-data', 'Data Functional Design')
        ],
        default='businesscontext'
        )

    code_search_json = HiddenField('Code Search JSON')

    code_mod_input = SelectField('Code Modification Input', choices=[
        ('dummy', 'Select Key Input'),
        ('functional-ui', 'UI Functional Design'),
        ('functional-services', 'Services Functional Design'),
        ('functional-data', 'Data Functional Design'),
        ('highlevel-ui', 'UI High Level Design'),
        ('highlevel-services', 'Services High Level Design'),
        ('highlevel-data', 'Data High Level Design'),
        ('lowlevel-ui', 'UI Low Level Design'),
        ('lowlevel-services', 'Services Low Level Design'),
        ('lowlevel-data', 'Data Low Level Design')
        ],
        default='functional'
        )

    get_related_files_button = SubmitField('Get Related Files')
    relatedfiles_textarea = HiddenField('Related Files')
    selectedfile = HiddenField('Selected File')
    relatedfiles_select = SelectField('Related Files', choices=[
        ('dummy', 'Select Related File')
        ]
        )
    get_code_button = SubmitField('Get Code')
    asis_code = TextAreaField('Current Code',validators=[Length(max=15000)])
    modify_code_button = SubmitField('Modify Code')
    tobe_code = TextAreaField('Modified Code',validators=[Length(max=15000)])
    push_code_button = SubmitField('Push Code to Repo')

    #Stream CheckBox
    streamOpenAICheckBox = BooleanField('Stream Output', default=False)

    # List of Hidden Fields
    currentevent = HiddenField('Current Event')
    selected_tab = HiddenField('Selected Tab')
    selected_link = HiddenField('Selected Link')
    selected_llmmodel = HiddenField('Selected LLM Model')
    unique_name = HiddenField('Unique Name Graph')
    
