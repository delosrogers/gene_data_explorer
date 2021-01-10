from flask import redirect, request, url_for, render_template, request, make_response, g, send_from_directory, session
import platform
import gene_data_explorer.service as service
from gene_data_explorer import app, db
from gene_data_explorer.credentials import *
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
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app.config['TESTING']=False


app.secret_key = os.environ.get("SECRET_KEY")
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
    print(User.authorized_email(users_email), "authed email")
    print(users_email)
    user = User.get(unique_id)
    if user.authed or UserManagement.is_email_authorized(users_email):
        print(user)
        if user is None:
            user = User(id=unique_id, email=users_email, username=users_name, user_type="user", authed=True)
            user.create()
    else:
        if user is None:
            user = User(id=unique_id, email=users_email, username=users_name, user_type="user", authed=False)
            user.create()
    login_user(user)
    next_page = session.get('login_redirect')
    session.pop('login_rediriect', None)
    print (next_page)
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    #if(users_email == 'mattiasdelosrios@berkeley.edu'):
    print('loging in')
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
def manage_users():
    form = Admin_email_management_form()
    all_users = User.get_all_users()
    if request.method == 'POST' and form.validate_on_submit():
        if form.add_or_remove == 'add': 
            Authorized_user_emails.add_email(form.email.data)
        elif form.add_or_remove == 'remove':
            Authorized_user_emails.add_email(form.email.data)
    return render_template('admin.html', form=form,
            column_names=all_users.columns.values, row_data=list(all_users.values.tolist()), zip=zip)


@app.route('/mine', methods=['GET', 'POST']) #allow both GET and POST requests
@login_required
def mine():
    return service.db_form(request, "mine.html")


@app.route('/rnai', methods=['GET', 'POST'])
def rnai():
    return service.db_form(request, "RNAi.html")


@app.route('/analysis_info')
def serve_info():
    return pd.read_csv("templates/analysis_info.csv").to_html()


@app.route('/database_info')
def serve_db_info():
    return service.get_db_info().to_html()


@app.route('/gene_info')
def gene_info():
    gene = request.args.get("gene")
    return service.get_gene_info(gene)


@app.route('/node_modules/<path:filename>', methods=["GET"])
def serve_libraries(filename):
    return send_from_directory(
        app.root_path + '/node_modules/',
        filename, conditional=True
        )


# @app.route('/sql', methods=['GET', 'POST'])
# def custom_sql():
#     if request.method == 'POST':
#         query = request.form
#         result, sql_statement = service.parse_custom_query(query)
#         resp = make_response(result.to_csv(sep="\t"))
#         resp.headers["Content-Disposition"] = "attachment; filename=result.txt"
#         resp.headers["Content-Type"] = "text/csv"
#         if query['download_type']=="tsv":
#             return resp
#         else:
#             return '''{}<br> the SQL statement used was:<br>{}'''.format(result.to_html(), sql_statement)
#     return render_template("sql.html") 


if __name__ == "__main__":        # on running python app.py
    #port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0')
