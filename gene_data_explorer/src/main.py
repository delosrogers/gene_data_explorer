from flask import Flask, render_template, request, make_response, g          # import flask
from flask_sqlalchemy import SQLAlchemy
import platform
import service




      #import service after app and db are initialized


@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return render_template("index.html")         # which returns "hello world"

@app.route('/mine', methods=['GET', 'POST']) #allow both GET and POST requests
def mine():
    g.db = db
    return service.db_form(request, "mine.html")

@app.route('/rnai', methods=['GET', 'POST'])
def rnai():
    g.db = db
    return service.db_form(request, "RNAi.html")

@app.route('/analysis_info')
def serve_info():
    return pd.read_csv("templates/analysis_info.csv").to_html()

@app.route('/database_info')
def serve_db_info():
    return service.get_db_info().to_html()

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
    
    def init_app():
        global app
        global db
        app = Flask(__name__)
        with open ("credentials.txt","r") as myfile: passwd = myfile.readlines()[0]
        if platform.system() == 'Linux':
            host = 'gene_data_mysql'
        else:
            host = 'localhost'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://web_app:{passwd}@{host}:3306/gene_data'.format(passwd = passwd, host=host)
        with app.app_context():
            db=SQLAlchemy(app)
        return [app, db]
    
    app.run(host = '0.0.0.0', port = 80, debug=True)