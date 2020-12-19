from flask import Flask           # import flask
from flask import render_template
from flask import request
from flask import make_response
import service
app = Flask(__name__)             # create an app instance
@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return render_template("index.html")         # which returns "hello world"

@app.route('/mine', methods=['GET', 'POST']) #allow both GET and POST requests
def mine():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        query = request.form

        result, sql_statement = service.parse_query(query)
        resp = make_response(result.to_csv(sep="\t"))
        resp.headers["Content-Disposition"] = "attachment; filename=result.txt"
        resp.headers["Content-Type"] = "text/csv"
        if query['download_type']=="tsv":
            return resp
        else:
            return '''{}<br> the SQL statement used was:<br>{}'''.format(result.to_html(), sql_statement)

    return render_template("mine.html")

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
      app.run(host = '0.0.0.0', port = 5001, debug=True)