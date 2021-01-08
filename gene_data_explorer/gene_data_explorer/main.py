from flask import redirect, request, url_for, render_template, request, make_response, g, send_from_directory
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

from gene_data_explorer.user import User


GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app.config['TESTING']=False


app.secret_key = os.environ.get("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

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
    user = User(id_=unique_id, username=users_name, email=users_email)
    if not(user.get(unique_id)):
        User.create(unique_id, users_name, users_email)
    #if(users_email == 'mattiasdelosrios@berkeley.edu'):
    print('loging in')
    print(user.id)
    login_user(user)
    print(user.is_authenticated)
    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("mine"))

@app.route("/")                   # at the end point /
def hello():
    print(current_user.username)                      # call method hello
    return render_template("index.html")         # which returns "hello world"


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
