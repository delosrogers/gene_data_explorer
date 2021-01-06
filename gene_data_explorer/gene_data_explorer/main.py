from flask import Flask, render_template, request, make_response, g          # import flask
from flask_sqlalchemy import SQLAlchemy
import platform
import gene_data_explorer.service as service
from gene_data_explorer import app


      #import service after app and db are initialized



@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return render_template("index.html")         # which returns "hello world"

@app.route('/mine', methods=['GET', 'POST']) #allow both GET and POST requests
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