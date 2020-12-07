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
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        query = request.form
        
        result = service.parse_query(query)
        resp = make_response(result.to_csv(sep="\t"))
        resp.headers["Content-Disposition"] = "attachment; filename=result.txt"
        resp.headers["Content-Type"] = "text/csv"
        if query['download_type']=="tsv":
            return resp
        else:
            return '''{}'''.format(result.to_html())

    return '''<form method="POST">
                  <h3>What form do you want your results?</h3>
                  <select name="download_type">
                    <option value="html">HTML</option>
                    <option value="tsv"> TSV </option>
                  </select>
                  <h3>Dataset:</h3>
                  <input type="checkbox" name ="dataset" value=tph1p_v_N2> tph-1p </input>
                  <input type="checkbox" name ="dataset" value=dat1p_v_N2> tph-1p </input>
                  <input type="checkbox" name ="dataset" value=rab3p_v_N2> rab-3p </input>
                  <h3><i>columns:</i><h3>
                  <input type="checkbox" name="column" value="baseMean"> <label> baseMean </label>
                  <input type="checkbox" name="column" value="log2FoldChange"> <label> log2FoldChange </label>
                  <input type="checkbox" name="column" value="lfcSE"> <label> lfcSE </label>
                  <input type="checkbox" name="column" value="stat"> <label> stat </label>
                  <input type="checkbox" name="column" value="pvalue"> <label> pvalue </label>
                  <input type="checkbox" name="column" value="padj"> <label> padj </label>
                  <br>
                  genes:<br>
                  <textarea name="genes"></textarea>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == "__main__":        # on running python app.py
      app.run(debug=True)