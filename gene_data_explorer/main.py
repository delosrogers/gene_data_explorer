from flask import redirect, request, url_for, render_template, request, make_response, g, send_from_directory, session
import platform
import gene_data_explorer.service as service
from gene_data_explorer.service import UserManagement
from gene_data_explorer import app, db
from gene_data_explorer.config import *
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
import json
from gene_data_explorer.models import Admin_email_management_form, Authorized_user_emails, User
from flask_bootstrap import Bootstrap
from werkzeug.urls import url_parse
from functools import wraps
import secrets

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app.config['TESTING'] = True
app.config['LOGIN_DISABLED'] = os.getenv("LOGIN_DISABLED", "False") == "True"

app.secret_key = secrets.token_bytes(32)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
bootstrap = Bootstrap(app)
login_manager.login_view = 'login'

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    try:
        return requests.get(GOOGLE_DISCOVERY_URL).json()
    except:
        print('something went wrong with google authentication')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def authentication_required(func):
    def wrapper():
        print(app.config)
        if app.config['LOGIN_DISABLED']:
            return func()
        elif current_user.is_authenticated():
            return func()
        else:
            return "not authenticated"
    wrapper.__name__ = func.__name__
    return wrapper


def admin_required(func):
    def wrapper():
        if current_user.is_authenticated() and current_user.user_type == "admin":
            return func()
        else:
            return "not authenticated"
    wrapper.__name__ = func.__name__
    return wrapper


# def login_required(role="ANY"):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated_view(*args, **kwargs):
#             if not current_user.is_authenticated():
#                 return login_manager.unauthorized()
#             if ((current_user.user_type != role) and (role != "ANY")):
#                 return login_manager.unauthorized()
#             return fn(*args, **kwargs)
#         return decorated_view
# #    return wrapper

@app.route("/login")
def login():
    session['login_redirect'] = request.args.get('next')
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        print("User email not available or not verified by Google.", 400)
        return
    user = User.get(unique_id)
    print(user, "user in callback")
    if UserManagement.is_email_authorized(users_email):
        print(user)
        if user is None:
            user = User(id=unique_id, email=users_email,
                        username=users_name, user_type="user", authed=True)
            user.create()
    else:
        print("made it to else in callback")
        if user is None:
            user = User(id=unique_id, email=users_email,
                        username=users_name, user_type="user", authed=False)
            user.create()
    login_user(user)
    next_page = session.get('login_redirect')
    session.pop('login_rediriect', None)
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    return redirect(next_page)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")                   # at the end point /
def index():
    if current_user.is_authenticated:
        print(current_user.username)
    return render_template("index.html")


@app.route("/admin", methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    form = Admin_email_management_form()
    if form.validate_on_submit():
        if form.add_or_remove.data == 'add':
            UserManagement.authorize_email(form.email.data)
        elif form.add_or_remove.data == 'remove':
            UserManagement.deauthorize_email(form.email.data)
    all_users = User.get_all_users()
    return render_template('admin.html', form=form,
                           column_names=all_users.columns.values, row_data=list(all_users.values.tolist()), zip=zip)


# allow both GET and POST requests
@app.route('/mine', methods=['GET', 'POST'])
@login_required
@authentication_required
def mine():
    if request.method == 'POST':  # this block is only entered when the form is submitted
        query = request.form

        result, sql_statement = service.parse_RNAseq_query(query)
        result = result.apply(
            service.replace_empty_gene_name_with_wbid_or_sequence, axis=1)
        if query.get('sequence_names') != "True":
            result = result.drop('genes.sequence', axis=1)
        download_type_switch = {
            'tsv': service.send_download,
            'clustergrammer': service.make_clustergrammer,
            'html': service.render_html_table,
        }
        resp = download_type_switch[query.get('download_type')](result)
        return resp
    else:
        return render_template('mine.html')


@app.route('/rnai', methods=['GET', 'POST'])
def rnai():
    if request.method == 'POST':  # this block is only entered when the form is submitted
        query = request.form

        result, sql_statement = service.parse_RNAi_query(query)
        result = result.apply(
            service.replace_empty_gene_name_with_wbid_or_sequence, axis=1)
        if query.get('sequence_names') != "True":
            result = result.drop('genes.sequence', axis=1)
        download_type_switch = {
            'tsv': service.send_download,
            'html': service.render_html_table,
        }
        resp = download_type_switch[query.get('download_type')](result)
        return resp
    else:
        return render_template('RNAi.html')
        


@app.route('/analysis_info')
def serve_info():
    return pd.read_csv("templates/analysis_info.csv").to_html()


@app.route('/database_info')
@login_required
@authentication_required
def serve_db_info():
    return service.get_db_info().to_html()


@app.route('/gene_info')
@login_required
@authentication_required
def gene_info():
    gene = request.args.get("gene")
    return service.get_gene_info(gene)


@app.route('/node_modules/<path:filename>', methods=["GET"])
def serve_libraries(filename):
    return send_from_directory(
        app.root_path + '/node_modules/',
        filename, conditional=True
    )


if __name__ == "__main__":        # on running python app.py
    #port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', use_reloader=False)
