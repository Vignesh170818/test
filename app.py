'''Main Flask Application for the Bot'''
from docx import Document
import io
import shutil
import uuid
import os
import asyncio
import hashlib
from concurrent.futures import ThreadPoolExecutor
import datetime
import logging
import traceback
import json
from uuid import uuid1
import bleach
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    send_file,
    flash,
    redirect,
    url_for,
    session,
    jsonify
    )
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from plugins.bpmservice.controller import GenLiteBPM
from plugins.bpmservice.model import BPMInput
from bpmtree.vectorsearch.filesearch import PickleFileSearch
from bpmtree.util.treeview import generate_jstree_json
from bpmtree.util.util import json_to_stringbpm
from appext.orchestration.epic import (
    generate_epic,
    review_epic,
    apply_review_epic
    )
from appext.orchestration.feature import (
    generate_feature,
    expand_feature
    )
from appext.orchestration.userstory import (
    generate_userstory,
    expand_userstory,
    generate_userstory_tasks
    )
from appext.orchestration.design import (
    generate_functional_design,
    generate_high_level_design,
    generate_low_level_design,
    generate_functional_design_from_image
    )
from appext.orchestration.code import generate_code
from appext.orchestration.componentdiagram import generate_componentdiagram
from appext.orchestration.deployment import generate_deployment
from appext.orchestration.test import (
    generate_test_scenarios,
    generate_test_cases,
    generate_test_scripts,
    generate_test_scripts_tool
    )
from appext.orchestration.architecture import generate_architecture
from applicationcontext.utils import get_application_context
from genliteappext.genliteform import GenLiteMainForm
from settings import app_json
from downloadtemplates import worddocgenerator
from msal.exceptions import MsalServiceError
from adauth.config import msal_config,msal_client
from logger_utils.get_logger import get_logger
from prefix_middleware import PrefixMiddleware
from functools import wraps
from llm_output_parsers.parser import *
from sqlite_handler.handler import *
from tool_integration.integration import get_entityData
from appext.orchestration.graph import get_graph

logger = get_logger("GenLiteApp")
logger.info("App Started Initialization")
logger.info(f"msal_config = {msal_config}")
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)

app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app_json.get("SUFFIX",'/core'))

app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = 3600 # 60 minutes
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024 #5 MB
LOGOUT_URIPATH = "https://login.microsoftonline.com/{tenant_id}/oauth2/logout"
LOGOUT_URIPATH += "?post_logout_redirect_uri"
LOGOUT_URIPATH += "={base_uri}/loggedout"
app.config['OIDC_LOGOUT_URI'] = LOGOUT_URIPATH
Session(app)

session_dictionary = {}

cors = CORS(app, resources={
    r"/*": {
        "origins": app_json["AllowedOrigins"],
        "methods": ["GET", "POST"],  # specify which methods are allowed
        "expose_headers": ["Authorization"],  # specify which headers to expose to the browser
        "allow_headers": [
            "Content-Type",
            "Authorization"
            ],  # specify which headers are allowed in the request
        "supports_credentials": True  # allow cookies to be included in the requests
    }
})

csrf = CSRFProtect(app)
csrf.init_app(app)

executor = ThreadPoolExecutor(max_workers=4)  # Adjust max_workers as needed

async def run_sync_in_thread_pool(func, *args):
    '''Run a synchronous function in a thread pool.'''
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, func, *args)




def validate_origin(func):
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if request.method != 'POST':
            return jsonify({"response": "Invalid Request"}),405
        if 'Origin' in request.headers:
            origin = request.headers['Origin']
            allowed_origins = app_json['AllowedWebsites']
            for i in allowed_origins:
                if  i in origin:
                # If the origin is allowed, proceed to the endpoint function
                    return await func(*args, **kwargs)
            
            return jsonify({'error': 'Invalid origin'}), 403  # Forbidden
        else:
            return jsonify({'error': 'Origin header missing'}), 400  # Bad request
    return wrapper





@app.route('/loggedout',methods=['GET','POST'])
def logged_out():
    session.clear()
    return render_template('logout.html')

@app.route("/login",methods=["GET","POST"])
def login():
    logger.info(f"session_id : {session.sid}")
    try:
        logger.info("Request for login page recieved")
        auth_url = msal_client.get_authorization_request_url(
            scopes=msal_config["scope"],
            redirect_uri= msal_config["redirect_uri"],
        )
        return redirect(auth_url)
    except MsalServiceError as e:
        tb = traceback.format_exc().split("\n")
        #logger.error(f"{str(e)} error occured while login: Traceback: {str(tb)}")
        return render_template("not_authenticated.html",error_message=str(e))


    except Exception as e:
        tb = traceback.format_exc().split("\n")
       # logger.error(f"{str(e)} error occured while logging: Traceback: {str(tb)}")
        return render_template("not_authenticated.html",error_message=str(e))


@app.route("/unauthorized")
def unauthorized():
    return render_template("not_authenticated.html")

@app.route("/get_token")
def get_token():
    if 'code' in request.args:
        try:
            logger.info("Request for gettoken page recieved")
            token_response = msal_client.acquire_token_by_authorization_code(
                code=request.args["code"],
                scopes=msal_config["scope"],
                redirect_uri=msal_config["redirect_uri"],
            )
             
            # Get user information from the /me endpoint
            #logger.info(f"token_response:{token_response}\n\n\n\n") 
            if 'id_token_claims' in token_response:    
                #session["user"] = token_response["id_token_claims"]['name']
                session['user_name']= token_response["id_token_claims"]['preferred_username']
                session_dictionary[session['user_name']] = True
                logger.info(f"session_id : {session.sid}")
                
                logger.info(f"session success:{session} \n\n\n\n")
            else:
                logger.info(f"id_token_claims not in token_response :{token_response}")
                session['user_id'] = str(uuid1())
            return redirect(url_for("index"))
        except Exception as e:
            tb = traceback.format_exc().split("\n")
           # logger.error("ERROR WHILE AUTHENTICATING...............")
            #logger.info(f"{str(e)} occured.Tracback:{str(tb)}")
            #logger.error(f"msal_config:{msal_config}")
            
    #session['user_id'] = str(uuid1())
    #logger.info(f"get_token:{session}")
    return redirect(url_for("index"))

@app.route('/', methods=["GET", "POST"])
def index():
    '''Index page'''
    logger.info("Request for index page recieved")
    logger.info(f"session : {session}")
    logger.info(f"session_id : {session.sid}")

    if msal_config.get('auth_enabled','').lower()=='true':
        if 'user_name' not in session  :
            logger.info("username not present in session. Redirected to login.")
            return redirect(url_for("login"))

        # elif session['user_name'] not in session_dictionary:
        #     logger.info("username is present in session but not in sess_dict. Redirected to login.")
        #     return redirect(url_for("login"))

        # and not session.get("user_name") and session.get('user_name') not in session_dictionary:
        # logger.info("Session not present. Redirected to login.")
        # return redirect(url_for("login"))


    logger.info(f"user_session present : {session}")
    logger.info(f"session_dictionary : {session_dictionary}")
    #session_dictionary[session['user_name']] = True
    form = GenLiteMainForm()
    form.selected_tab.data = 'inputTab'
    form.selected_link.data = 'input-link'
    return render_template(
        'index.html',
        form=form,
        cdnjsdomain='cdnjs.cloudflare.com',
        cdnjsdelivrdomain='cdn.jsdelivr.net',
        session_timeout = app.config['PERMANENT_SESSION_LIFETIME']
        )

@app.route('/favicon.ico')
def favicon():
    '''Favicon'''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/style.css')
def stylecss():
    '''Favicon'''
    logger.info('Inside stylecss')
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'style.css', mimetype='text/css')

@app.route('/gen_lite.js')
def genlitejs():
    '''Favicon'''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'gen_lite.js', mimetype='text/javascript')

@app.route('/logo.png')
def logo():
    '''Favicon'''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'logo.png', mimetype='image/png')

@app.route('/robots.txt')
def static_from_root():
    '''Favicon'''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt', mimetype='text/plain')

@app.route('/msword.png')
def msword():
    '''Favicon'''
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'msword.png', mimetype='image/png')

@app.errorhandler(404)
def page_not_found(e):
    '''Page Not Found'''
    logger.error('Inside page_not_found %s', e)
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    '''Internal Server Error'''
    logger.error('Inside internal_server_error %s', e)
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(e):
    '''Forbidden'''
    logger.error('Inside forbidden %s', e)
    return render_template('403.html'), 403

@app.after_request
def after_request(response):
    '''After Request'''
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    csp = (
    # "default-src 'self' 'unsafe-eval' 'unsafe-inline' *.accenture.com; "
    "default-src 'self' 'unsafe-eval' 'unsafe-inline' *.accenture.com; media-src data:; "
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' *.cloudflare.com *.jsdelivr.net; "
    "worker-src 'self' blob: *.accenture.com; " 
    "font-src 'self' 'unsafe-inline' 'unsafe-eval' *.cloudflare.com *.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline' *.cloudflare.com *.jsdelivr.net; "
    "img-src 'self' *.accenture.com *.cloudflare.com *.jsdelivr.net data:; "
    "connect-src 'self' *.accenture.com; "
    "upgrade-insecure-requests; "
    "block-all-mixed-content;"
    )
    response.headers["Content-Security-Policy"] = csp
    response.headers["X-Content-Type-Options"] = "nosniff"
    # response.headers["Referrer-Policy"] = "no-referrer"
   # response.headers['Cache-Control'] = 'no-store'
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public,max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    #response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers['server'] = 'GenLite'
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response

@app.before_request
def check_session_timeout():
    '''Check Session Timeout'''
    now = datetime.utcnow()

    last_activity = session.get('last_activity')
    if last_activity:
        diff = now - datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')
        if diff.total_seconds() > app.config['PERMANENT_SESSION_LIFETIME']:
            session.clear()
            flash('Session timed out!', 'danger')
            return redirect(url_for('logout'))

    session['last_activity'] = str(now)


@app.route('/uploadwireframe', methods=['GET', 'POST','OPTIONS'])
@csrf.exempt
@validate_origin
async def uploadwireframe():
    '''Upload Wireframe'''
    if request.method == 'POST':

        if 'wireframe_image' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['wireframe_image']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            if len(file.read()) > MAX_FILE_SIZE_BYTES:
                return jsonify({"error": "File size exceeds the maximum limit of 5MB"}), 400
            file.seek(0)

            _, extension = os.path.splitext(file.filename)
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            if extension.lower() not in allowed_extensions:
                return jsonify({"error": "Uploaded file is not an image"}), 400
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.root_path, 'uploadfiles', filename)
            file.save(filepath)
            logger.info('File uploaded successfully')
            fdtext = await generate_functional_design_from_image(filepath)
            return jsonify({"response": fdtext})
    return jsonify({"error": "Invalid Request"}), 400

@app.route('/bpmtreeview', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def get_tree_data():
    '''Returns data from Neo4j database.'''
    print("Inside get_tree_data")
    if request.method == 'POST':
        data = request.get_json()
        # Extract the 'treeviewindustry' value from the JSON data
        treeviewindustry = data['treeviewindustry']
        # Clean the input
        treeviewindustry = bleach.clean(treeviewindustry)
        is_valid=validate_length(treeviewindustry)
        treeviewdata = ""
        if is_valid is True:
            treeviewdata = await asyncio.to_thread(generate_jstree_json, treeviewindustry)
        else:
            flash('Input passed has exceeded the maximum limit','info')
            treeviewdata = ""
        return jsonify({"response":  treeviewdata})
    else:
        return jsonify({"response": "Invalid Request"})

@app.route('/logout')
def logout():
    '''Logout'''
    logger.info("Request for Logout page recieved")
    preferred_username = session.get("user_name",None)
    logger.info(f"session_id : {session} ,{session.sid}")
    if preferred_username: 
        accounts = msal_client.get_accounts(preferred_username)
        logger.info(f"@@@@ List of MSAL Account BEFORE signed out from MSAL is:{accounts}")
        if accounts:
            account=accounts[0]
            logger.info(f"$$$$ The single Account signed out from MSAL is:{account}")
            msal_client.remove_account(account)
            accounts = msal_client.get_accounts(preferred_username)
            logger.info(f"&&&& List of MSAL Account AFTER signed out from MSAL is:{accounts}")
    if session.get('user_name') and session['user_name'] in session_dictionary :
        del session_dictionary[session['user_name']]
    session.clear()
    session['logout']="True"

    logger.info(f"session cleared: {session}")
    logger.info(f"session_id : {session} ,{session.sid}")
    # Redirect to Azure AD logout URL
    tenant_id : str | None = msal_config["tenant_id"]
    base_uri : str | None = msal_config["base_uri"]
    #tenant_id = os.environ.get("MICROSOFT_PROVIDER_TENANT_ID")
    logout_url = LOGOUT_URIPATH.replace("{tenant_id}", tenant_id).replace("{base_uri}", base_uri)
    resp = redirect(logout_url)
    resp.set_cookie('session', '', expires=0)
    return resp

@app.route('/changeapplicationcontext', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def changeapplicationcontext():
    '''Change Application Context'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        industry = form.industry.data
        try:
            applicationcontext = get_application_context(industry)
            return jsonify({"response": applicationcontext})
        except FileNotFoundError:
            return jsonify({"response": "Application Context Not Found"})
    else:
        return jsonify({"response": "Invalid Request"}),405

@app.route('/getbusinesscontext', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def getbusinesscontext():
    '''Get Business Context'''
    try:
        popovercontent = ""
        if request.method == 'POST':
            form = GenLiteMainForm()
            industry = form.industry.data
            applicationcontext = form.ecosystem_context.data
            scope_vision = form.scope_vision.data

            # Clean the input
            industry = bleach.clean(industry)
            applicationcontext = bleach.clean(applicationcontext)
            scope_vision = bleach.clean(scope_vision)

            is_valid= validate_length(
                industry,
                applicationcontext,
                scope_vision
                )

            llmplatform = form.llm_platform_options.data
            logger.info("Selected LLM Platform: %s", llmplatform)

            if is_valid is True:
                bpmobject = GenLiteBPM(
                    industry=industry,
                    llmplatform=llmplatform
                    )

                inputdata = BPMInput(
                    businesscontext="",
                    highlevelreq=scope_vision,
                    applicationcontext=applicationcontext
                    )

                generatedbpm  = await asyncio.to_thread(
                    bpmobject.bpmjson_generate,
                    inputdata
                    )

                popovercontent += "Entities Identified from High Level Requirement: "
                popovercontent += "<br>"
                stringbpm = await asyncio.to_thread(json_to_stringbpm, generatedbpm)
                popovercontent += stringbpm
                popovercontent += "<br>"

                combinedtext = generatedbpm + scope_vision

                vectorsearch = PickleFileSearch(industry=industry)

                multibusinesscontext = await asyncio.to_thread(
                    vectorsearch.get_business_context,
                    combinedtext,
                    3
                    )

                #multibusinesscontext split by | and for loop
                counter = 0
                businesscontext = ""
                for eachrow in multibusinesscontext.split("|"):
                    # if eachrow contains ~ then split by ~ and get the context and score
                    if "~" in eachrow:
                        context = eachrow.split("~")[0]
                        if counter == 0:
                            businesscontext = context
                        context = context.replace(
                            "Business Sub Domain:",
                            "<br>Business Sub Domain:"
                            )
                        context = context.replace(
                            "Business Capability:",
                            "<br>Business Capability:"
                            )
                        context = context.replace(
                            "Business Sub Capability:",
                            "<br>Business Domain:"
                            )
                        context = context.replace("Workflow:", "<br>Workflow:")
                        score = eachrow.split("~")[1]
                        if counter == 0:
                            businesscontext = context
                        popovercontent += f"Mapped Business Context {counter + 1} with {score}"
                        popovercontent += "<br>"
                        popovercontent += f"<p>{context}</p>"
                        # popovercontent += "<br>"
                        counter += 1

                bpmobject1 = GenLiteBPM(industry=industry, llmplatform=llmplatform)
                inputdata = BPMInput(
                    businesscontext=businesscontext,
                    highlevelreq=scope_vision,
                    applicationcontext=applicationcontext
                    )
                process_flow_mapping = await asyncio.to_thread(
                    bpmobject1.processflow_generate,
                    inputdata
                    )

            return jsonify(
                {
                    "popovercontent": popovercontent,
                    "process_flow_mapping": process_flow_mapping,
                    "businesscontext": businesscontext
                }
                )
        else:
            return jsonify({"response": "Invalid Request"}),405
    except Exception as e:
        err = str(e)
        tb = traceback.format_exc().split("\n")
        tb = str(tb)
        logger.error(f'{err} occurred while getting businesscontext, traceback:{tb}')
        popovercontent = err
        process_flow_mapping = err
        businesscontext = ''
        return jsonify(
            {
                "popovercontent": popovercontent,
                "process_flow_mapping": process_flow_mapping,
                "businesscontext": businesscontext
            }
            )


@app.route('/generateepic', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generateepic():
    '''Generate Epic'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        form = cleanse_form(form)
        epic = await generate_epic(form)
    else:
        epic = "Invalid Request"
    if form.streamOpenAICheckBox.data:
        return epic
    else:
        return jsonify({"response": epic})
    
@app.route('/getentitydata', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def getentitydata():
    '''Get Entity Details'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        form = cleanse_form(form)
        entity_type = form.entity_type.data
        try:
            external_id = (form.epic_external_id.data if entity_type == 'epic' 
               else form.feature_external_id.data if entity_type == 'feature' 
               else form.user_story_external_id.data if entity_type == 'userstory' 
               else None)
            is_valid= True
            is_valid=validate_id_length(external_id)
            if is_valid==True:
                details1,details2=get_entityData(external_id,entity_type)
                response_data = {}

                if entity_type == 'epic':
                    response_data['epic_user_story'] = details2
                    form.epic_external_id.data = external_id
                elif entity_type == 'feature':
                    response_data['selected_feature'] = details1
                    response_data['feature_user_story'] = details2
                    form.feature_external_id.data = external_id
                elif entity_type == 'userstory':
                    response_data['selected_user_story'] = details1
                    response_data['user_story_abstract'] = details2
                    form.user_story_external_id.data = external_id
                
                responsetype = 'success'
                return jsonify({"response": response_data,"responsetype": responsetype})
            else:
                returnresponse = "Error"
                responsetype = "error"
                return jsonify({"response": returnresponse,"responsetype": responsetype, "Epic_External_Id": form.epic_external_id.data})
        except Exception as e:
                flash_message = f" {str(e)} : {external_id}"
                return jsonify({"response": flash_message,"responsetype": "info", "External_Id": external_id})

@app.route('/resetentitydata', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def resetentitydata():
    '''Reset Entity Details'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        entity_type = form.entity_type.data
        try:
            form.user_story_external_id.data=''
            form.user_stories_list.data = ''
            form.selected_user_story.data=''
            form.user_story_abstract.data=''
            if entity_type == 'feature' or entity_type == 'epic':
                form.feature_external_id.data=''
                form.features_list.data = ''
                form.selected_feature.data=''
                form.feature_user_story.data=''
                if entity_type == 'epic':
                    form.epic_external_id.data=''
                    form.epic_user_story.data=''
            return jsonify({"response": 'Reset successful' ,"responsetype": "success"})
        except Exception as e:
            flash_message = f" {str(e)} :Error"
            return jsonify({"response": flash_message,"responsetype": "info"})

@app.route('/reviewepic', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def reviewepic():
    '''Review Epic'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        form = cleanse_form(form)
        reviewcomments = await review_epic(form)
    else:
        reviewcomments = "Invalid Request"

    return jsonify({"response": reviewcomments})

@app.route('/applyepicreview', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def applyepicreview():
    '''Apply Epic Review'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        modifiedepic = await apply_review_epic(form)
    else:
        modifiedepic = "Invalid Request"

    return jsonify({"response": modifiedepic})

@app.route('/generatefeature', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatefeature():
    '''Generate Feature'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        featurecontent = await generate_feature(form)
        return jsonify({"response": featurecontent})
    else:
        return jsonify({"response": "Invalid Request"})

@app.route('/expandfeature', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def expandfeature():
    '''Expand Feature'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        featurecontent = await expand_feature(form)
        return jsonify({"response": featurecontent})
    else:
        return jsonify({"response": "Invalid Request"})

@app.route('/generateuserstories', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generateuserstories():
    '''Generate User Stories'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        returnresponse = await generate_userstory(form)
        return jsonify({"response": returnresponse})
    else:
        return jsonify({"response": "Invalid Request"})

@app.route('/expanduserstory', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def expanduserstory():
    '''Expand User Story'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        expandeduserstory = await expand_userstory(form)
        tasksforuserstory = await generate_userstory_tasks(form)
        returnresponse = expandeduserstory + "\n" + tasksforuserstory
        return jsonify({"response": returnresponse})
    else:
        return jsonify({"response": "Invalid Request"})

def register_user_request_json(epic_checksum,feature_checksum,json_data,status,us_checksums):
    file_dict = json_data
    req_uid = str(uuid1())
   
    status= insert_user_request(req_uid, file_dict,status=status,epic_checksum=epic_checksum,feature_checksum=feature_checksum,us_checksums=us_checksums)
    if status==False:
        response=None
    else:
        response = req_uid
    return response

@app.route('/consolidateworkitems', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def consolidateworkitems():
    '''Consolidate Workitems'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        
        returnresponse = ""
        form_epic_user_story = form.epic_user_story.data
        form_feature_user_story = form.selected_feature.data
        userstories_list = form.user_stories_list.data
        form_selected_user_story = form.selected_user_story.data
        form_selected_user_story_abstract = form.user_story_abstract.data
        form_epic_external_id = form.epic_external_id.data
        epic_checksum = hashlib.md5(form_epic_user_story.encode('utf-8')).hexdigest()
        feature_checksum = hashlib.md5(form_feature_user_story.encode('utf-8')).hexdigest()
        if form_epic_user_story.strip() == "" or form_feature_user_story.strip() == "" or form_selected_user_story.strip() == "":
            returnresponse = "Epic/Feature/Userstories are not generated or Mandatory details are missing for same."
            responsetype = "error"
        else:
            us_checksum = hashlib.md5(form_selected_user_story.encode('utf-8')).hexdigest()
            acc_checksum = hashlib.md5(form_selected_user_story_abstract.encode('utf-8')).hexdigest()
            epic = parse_epic_abstract(form_epic_user_story)
            if 'Title' in epic:
                epic['Title'] =  epic['Title'].replace("\r",'')
                epic['Title'] =  epic['Title'].replace("\n",'')
                if form_epic_external_id:
                    epic['ExternalId'] = form_epic_external_id
            feature = parse_selected_feature2(form_feature_user_story)
            userstory = parse_userstory_abstract(form_selected_user_story_abstract)
            if feature and form.feature_external_id.data:
                   feature['ExternalId'] = form.feature_external_id.data
            userstory_dict = {}
            form_selected_user_story = form_selected_user_story.replace("\r","")
            form_selected_user_story = form_selected_user_story.replace("\n","")
            us_pattern = r'User Story\s*\d+\s*:'
            import re
            form_selected_user_story = re.sub(us_pattern, '', form_selected_user_story)
            userstory_dict["Title"] = form_selected_user_story
            acc_pattern = r'Acceptance Criteria\s*:\s*'
            userstory['Acceptance Criteria'] = re.sub(acc_pattern,'',userstory['Acceptance Criteria']) if 'Acceptance Criteria' in userstory else form_selected_user_story_abstract
            userstory_dict["Acceptance Criteria"] = userstory["Acceptance Criteria"] if 'Acceptance Criteria' in userstory else form_selected_user_story_abstract
            if userstory_dict and form.user_story_external_id.data:
                    userstory_dict['ExternalId'] = form.user_story_external_id.data
            userstory_dict["Tasks"]= userstory["Tasks"] if 'Tasks' in userstory else []
            user_request_id = form.user_request_id.data if 'user_request_id' in form else None
            user_request_found=False
            if user_request_id!=None or user_request_id!="":
                request_var=retrieve_user_request_for_session(user_request_id)
                if request_var!=None:
                    user_request_found=True
            if user_request_id is None or user_request_id== '' or user_request_found==False:
                logger.info(f"user_request not found in request form : {user_request_id}, hence creating new user_request")
                tool_queue_dict = {"Epics":[]}
                tool_queue_dict["Epics"].append(epic)
                tool_queue_dict["Epics"][0]["Features"] = [feature]
                tool_queue_dict["Epics"][0]["Features"][0]["UserStories"]= []
                tool_queue_dict["Epics"][0]["Features"][0]["UserStories"].append(userstory_dict)
                json_data = json.dumps(tool_queue_dict)
                us_checksums = json.dumps([(us_checksum,acc_checksum)])
                response = register_user_request_json(epic_checksum,feature_checksum,json_data,"BUILD",us_checksums=us_checksums)
                
                if response==False:
                    returnresponse = "DB error occured"
                    responsetype = "error"
                else:
                    form.user_request_id.data = response
                    logger.info(f"inserted a new user_request with user_request_id:{response}")
                    returnresponse = "Created new user_request and consolidated successfully."
                    responsetype = "success"
            else:
                user_request = retrieve_user_request_for_session(user_request_id)
                if epic_checksum!=user_request['epic_checksum'] or feature_checksum!=user_request['feature_checksum']:
                    tool_queue_dict = {"Epics":[]}
                    tool_queue_dict["Epics"].append(epic)
                    tool_queue_dict["Epics"][0]["Features"] = [feature]
                    tool_queue_dict["Epics"][0]["Features"][0]["UserStories"]= []
                    tool_queue_dict["Epics"][0]["Features"][0]["UserStories"].append(userstory_dict)
                    json_data = json.dumps(tool_queue_dict)
                    us_checksums = json.dumps([(us_checksum,acc_checksum)])
                    response = register_user_request_json(epic_checksum,feature_checksum,json_data,"BUILD",us_checksums=us_checksums)
                    form.user_request_id.data = response
                    logger.info("epic checksum or feature checksum changed, hence creating new user_request")
                    logger.info(f"inserted a new user_request with user_request_id:{response}")
                    returnresponse = "Checksum changed, hence  created new user_request and consolidated successfully."
                    responsetype = "success"
                else:
                    tool_queue_dict = json.loads(user_request['file_content'])
                    us_checksums = json.loads(user_request['userstories_checksum'])
                    dup_flag= False
                    for checksum in us_checksums:
                        if checksum[0]==us_checksum and checksum[1]==acc_checksum:
                            dup_flag=True
                    if dup_flag==False:
                        us_checksums.append([us_checksum,acc_checksum])
                        us_checksums = json.dumps(us_checksums)
                        tool_queue_dict["Epics"][0]["Features"][0]["UserStories"].append(userstory_dict)
                        file_content = json.dumps(tool_queue_dict)
                        response=update_user_request(user_request['request_id'],file_content=file_content,us_checksum=us_checksums)
                        if response==False:
                            returnresponse = "DB error Occured while consolidating in existing workitems."
                            responsetype = "error"
                        else:
                            form.user_request_id.data = user_request['request_id']
                            returnresponse = "Consolidated successfully in the existing epic and Feature!!!"
                            responsetype = "success"
                    else:
                        returnresponse = "Userstory already consolidated !!! (duplicated identified with checksum)"
                        responsetype = "info"
        return jsonify({"response": returnresponse,"responsetype": responsetype, "user_request_id": form.user_request_id.data})
    else:
        return jsonify({"response": "Invalid Request"})

@app.route('/mergeworkitems', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def mergeworkitems():
    '''Push To ALM'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        user_request_id = form.user_request_id.data
        status, user_request = retrieve_user_request_for_merge(user_request_id)
        if status==False:
            logger.error(f"request not found, all request ids in DB with status build: {user_request}")
            form.status_response.data = user_request
            flash_message = f" user request not found with user_request_id : {request.form['user_request_id']}"
            return jsonify({"response": "Please Consolidate First!!!" + flash_message,"responsetype": "info"})
        else:
             logger.info(f"status:{status}")
             form.user_request_id.data = user_request_id
             response = user_request['request_id']
             update_user_request(user_request['request_id'],status="NEW")
             return jsonify({"response": f"pushed to ALM with request_id:{response}","responsetype": "info"})

@app.route('/checkstatus', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def checkstatus():
    '''Check Status'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        request_id = form.user_request_id.data
        db_req = retrieve_user_request(request_id)
        file_content=''
        if db_req:
            status = db_req['status'] if 'status' in db_req else "Request Not available or error occured, please try again"
            status_reason=db_req["status_reason"] if 'status_reason' in db_req else "NOT FOUND"
            status_reason=status_reason.replace('\n', "")
            file_content = db_req['file_content'] if 'file_content' in db_req else ''
        else:
            status='Request not found'
            status_reason='Request not found'
        return jsonify({"response": f"Request Id: {request_id}\nStatus: {status}\n Status_reason: {status_reason}\n file_content:{file_content}","responsetype": "info"})

@app.route('/download_tool_queue', methods=['GET','POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def download_tool_queue():
    '''Download Tool Queue JSON'''
    if request.method == 'GET' or request.method == 'POST':
        form = GenLiteMainForm()
        cwd = os.getcwd()
        try:
            request_id = form.user_request_id.data
            if request_id:
                user_request = retrieve_user_request(request_id)
            if user_request is None:
                return jsonify({'error': 'Request not found'}), 400  # Bad request
            
            tool_queue_json = json.loads(user_request['file_content'])
            ts = get_time_stamp()
            file_name = f"GenLite_Workitems_{ts}.json"
            temp_file_path = os.path.join("/home/LogFiles", file_name)

            with open(temp_file_path, "w") as f:
                json.dump(tool_queue_json, f, indent=4)
            
            return jsonify({"temp_file_path": temp_file_path, "file_name": file_name})
            
        except Exception as e:
            return jsonify({'error': 'Error in downloading file'}), 400  # Bad request

@app.route("/download_tool_queue_file")
def download_tool_queue_file():
    file_name = request.args.get('file_name_json')
    cwd=os.getcwd()
    file_path =  os.path.join("/home/LogFiles",file_name)
 
    cache = io.BytesIO()
    with open(file_path, 'rb') as fp:
        shutil.copyfileobj(fp, cache)
        cache.flush()
    cache.seek(0)
    os.remove(file_path)
    file_name=file_name.split("__")[0]+".json"
    file_name = file_name.split(os.path.sep)[-1]
    return send_file(cache, as_attachment=True, download_name=file_name)

def get_time_stamp():
    current_time_stamp = datetime.now()
    datestamp = current_time_stamp.strftime("%d%b%Y")
    timestamp = current_time_stamp.strftime("%H%M")
    return datestamp+"_"+timestamp

@app.route('/generatefunctionaldesign', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatefunctionaldesign():
    '''Generate Functional Design'''
    if request.method == 'POST':
        form = GenLiteMainForm()

        funcdict = await generate_functional_design(form)
        uidesign = funcdict.get("uidesign")
        servicesdesign = funcdict.get("servicesdesign")
        datadesign = funcdict.get("datadesign")

        return jsonify(
            {
                "uidesign": uidesign,
                "servicesdesign": servicesdesign,
                "datadesign": datadesign
            }
        )

@app.route('/generatehighleveldesign', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatehighleveldesign():
    '''Generate High Level Design'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        hlddict = await generate_high_level_design(form)
        uidesign = hlddict.get("uidesign")
        servicesdesign = hlddict.get("servicesdesign")
        datadesign = hlddict.get("datadesign")

        return jsonify(
            {
                "uidesign": uidesign,
                "servicesdesign": servicesdesign,
                "datadesign": datadesign
            }
        )

@app.route('/generatedetaileddesign', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatedetaileddesign():
    '''Generate Detailed Design'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        llddict = await generate_low_level_design(form)
        uidesign = llddict.get("uidesign")
        servicesdesign = llddict.get("servicesdesign")
        datadesign = llddict.get("datadesign")

        return jsonify(
            {
                "uidesign": uidesign,
                "servicesdesign": servicesdesign,
                "datadesign": datadesign
            }
        )

@app.route('/generatecode', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatecode():
    '''Generate Code'''
    print("Inside generatecode")
    if request.method == 'POST':
        form = GenLiteMainForm()
        codedict = await generate_code(form)
        uicode = codedict.get("uicode")
        servicescode = codedict.get("servicescode")
        datacode = codedict.get("datacode")

        return jsonify(
            {
                "uicode": uicode,
                "servicescode": servicescode,
                "datacode": datacode
            }
        )

# @app.route('/generateunittesting', methods=['POST'])
# @csrf.exempt
# async def generateunittesting():
#     '''Generate Unit Testing'''
#     if request.method == 'POST':
#         form = GenLiteMainForm()
#         llmplatform = form.llm_platform_options.data
#         logger.info("Selected LLM Platform: %s", llmplatform)
#         codegenerator = CodeGenerator(form, llmplatform=llmplatform)
#         unit_test = await asyncio.to_thread(codegenerator.generate_unit_test)
#         return jsonify({"response": unit_test})
#     else:
#         return jsonify({"response": "Invalid Request"})

@app.route('/generatetestplan', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatetestplan():
    '''Generate Test Plan'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        test_plan = await generate_test_scenarios(form)
        return jsonify({"response": test_plan})

@app.route('/generatetestcases', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatetestcases():
    '''Generate Test Cases'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        test_cases = await generate_test_cases(form)
        return jsonify({"response": test_cases})

@app.route('/generatetestscripts', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatetestscripts():
    '''Generate Test Scripts'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        test_scripts = await generate_test_scripts(form)
        return jsonify({"response": test_scripts})

@app.route('/generatetooltestscripts', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatetooltestscripts():
    '''Generate Tool Test Scripts'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        tool_test_scripts = await generate_test_scripts_tool(form)
        return jsonify({"response": tool_test_scripts})

@app.route('/generatecomponentdiagram', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatecomponentdiagram():
    '''Generate Component Diagram'''
    print("Inside generatecomponentdiagram")
    if request.method == 'POST':
        form = GenLiteMainForm()
        componentdiagram = await generate_componentdiagram(form)
        componentdiagram = componentdiagram.replace("```mermaid", "")
        componentdiagram = componentdiagram.replace("```", "")
        return jsonify({"response": componentdiagram})

#########################################################

@app.route("/download_file_fdd")
def download_file_fdd():
    file_name = request.args.get('file_name_fdd')
    cwd=os.getcwd()
    file_path =  os.path.join(cwd,file_name)
 
    cache = io.BytesIO()
    with open(file_path, 'rb') as fp:
        shutil.copyfileobj(fp, cache)
        cache.flush()
    cache.seek(0)
    os.remove(file_path)
    file_name=file_name.split("__")[0]+".docx"
    file_name = file_name.split(os.path.sep)[-1]
    return send_file(cache, as_attachment=True, download_name=file_name)

@app.route('/download_fdd', methods=['POST'])
@csrf.exempt
async def generate_fdd_document():
    '''Generate Functional Design Doc'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        save_file_path = await worddocgenerator.create_fdd_doc(form)
 
        return jsonify(
            {
                "filepath": save_file_path
            }
        )        


@app.route("/download_file_hld")
def download_file_hld():
    file_name = request.args.get('file_name_hld')
    cwd=os.getcwd()
    file_path =  os.path.join(cwd,file_name)
 
    cache = io.BytesIO()
    with open(file_path, 'rb') as fp:
        shutil.copyfileobj(fp, cache)
        cache.flush()
    cache.seek(0)
    os.remove(file_path)
    file_name=file_name.split("__")[0]+".docx"
    file_name = file_name.split(os.path.sep)[-1]
    return send_file(cache, as_attachment=True, download_name=file_name)

@app.route('/download_hld', methods=['POST'])
@csrf.exempt
async def generate_hld_document():
    '''Generate Functional Design Doc'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        save_file_path = await worddocgenerator.create_hld_doc(form)
 
        return jsonify(
            {
                "filepath": save_file_path
            }
        )        

@app.route("/download_file_dld")
def download_file_dld():
    file_name = request.args.get('file_name_dld')
    cwd=os.getcwd()
    file_path =  os.path.join(cwd,file_name)
 
    cache = io.BytesIO()
    with open(file_path, 'rb') as fp:
        shutil.copyfileobj(fp, cache)
        cache.flush()
    cache.seek(0)
    os.remove(file_path)
    file_name=file_name.split("__")[0]+".docx"
    file_name = file_name.split(os.path.sep)[-1]
    return send_file(cache, as_attachment=True, download_name=file_name)

@app.route('/download_dld', methods=['POST'])
@csrf.exempt
async def generate_dld_document():
    '''Generate Functional Design Doc'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        save_file_path = await worddocgenerator.create_dld_doc(form)
 
        return jsonify(
            {
                "filepath": save_file_path
            }
        )  

'''END OF DOWNLOAD FOR FUNC,HIGH LEVEL AND DETAIL LEVEL'''
#########################################################    

@app.route('/generatearchitecture', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatearchitecture():
    '''Generate Architecture'''

    if request.method == 'POST':
        form = GenLiteMainForm()
        llmplatform = form.llm_platform_options.data
        logger.info("Selected LLM Platform: %s", llmplatform)
        archdict = await generate_architecture(form)
        uiarch = archdict.get("uiarch")
        servicesarch = archdict.get("servicesarch")
        dataarch = archdict.get("dataarch")

        return jsonify(
            {
                "uiarch": uiarch,
                "servicesarch": servicesarch,
                "dataarch": dataarch
            }
        )

@app.route('/generatedeployment', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def generatedeployment():
    '''Generate Deployment'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        deploymentdict = await generate_deployment(form)
        uideployment = deploymentdict.get("uideployment")
        servicesdeployment = deploymentdict.get("servicesdeployment")
        datadeployment = deploymentdict.get("datadeployment")

        return jsonify(
            {
                "uideployment": uideployment,
                "servicesdeployment": servicesdeployment,
                "datadeployment": datadeployment
            }
        )

def validate_id_length(external_id):
    char_count = len(external_id)
    if char_count >= 0:
        return True
    else:
        flash(f"Kindly provide the external id for getting details.", "info")
        return False

def validate_length(*args):
    '''Validate Length'''
    for string in args:
        char_count = len(string)
        if char_count > 40000:
            return False
    return True

def cleanse_form(inputform: GenLiteMainForm):
    '''Validate Form'''
    for eachfield in inputform:
        try:
            if eachfield.type == 'TextAreaField':
                if eachfield.data is not None:
                    eachfield.data = bleach.clean(eachfield.data)
        except TypeError as e:
            logger.error("Error: %s", e)
            logger.exception(e)
    return inputform

@app.route('/download_eco_doc', methods=['POST'])
@csrf.exempt
async def generate_eco_doc():
    '''Generate Functional Design Doc'''
    if request.method == 'POST':
        form = GenLiteMainForm()
        save_file_path = await worddocgenerator.download_doc(form)
 
        return jsonify(
            {
                "filepath": save_file_path
            }
        )        


@app.route('/getgraph', methods=['POST','OPTIONS'])
@validate_origin
@csrf.exempt
async def getgraph():
    '''Get Graph'''
    if request.method == 'POST':
        logger.info('Testing get graph')
        form = GenLiteMainForm()
        serviceCode = form.services_code.data
        result = await get_graph(form, serviceCode)
        return jsonify({"response":  result.generate_html()})
    

if __name__ == '__main__':
    app.run(
        port='9000',
        debug=True
        )
    
