from flask import Flask           # import flask
from flask import render_template
from flask import request
from flask import Response
import service
app = Flask(__name__)             # create an app instance
@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return render_template("index.html")         # which returns "hello world"

@app.route('/mine', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        query = request.form.to_dict()
        result = service.parse_query(query)
        Response(result.to_csv('resluts.csv'),mimetype="txt/plain")

        return '''{}'''.format(result.to_html())

    return '''<form method="POST">
                  <h1>Dataset</h1>
                  <h3><i>tph-1p:</i><h3>
                  <input type="checkbox" name="tph-baseMean" value="tph1p_v_N2.baseMean"> <label for="tph-baseMean"> baseMean </label><br>
                  <input type="checkbox" name="tph-log2FoldChange" value="tph1p_v_N2.log2FoldChange"> <label for="tph-log2FoldChange"> log2FoldChange </label><br>
                  <input type="checkbox" name="tph-lfcSE" value="tph1p_v_N2.lfcSE"> <label for="tph-lfcSE"> lfcSE </label><br>
                  <input type="checkbox" name="tph-stat" value="tph1p_v_N2.stat"> <label for="tph-stat"> stat </label><br>
                  <input type="checkbox" name="tph-pvalue" value="tph1p_v_N2.pvalue"> <label for="tph-pvalue"> pvalue </label><br>
                  <input type="checkbox" name="tph-padj" value="tph1p_v_N2.padj"> <label for="tph-padj"> padj </label><br>
                  <h3><i>dat-1p:</i><h3>
                  <input type="checkbox" name="dat-baseMean" value="dat1p_v_N2.baseMean"> <label for="dat-baseMean"> baseMean </label><br>
                  <input type="checkbox" name="dat-log2FoldChange" value="dat1p_v_N2.log2FoldChange"> <label for="dat-log2FoldChange"> log2FoldChange </label><br>
                  <input type="checkbox" name="dat-lfcSE" value="dat1p_v_N2.lfcSE"> <label for="dat-lfcSE"> lfcSE </label><br>
                  <input type="checkbox" name="dat-stat" value="dat1p_v_N2.stat"> <label for="dat-stat"> stat </label><br>
                  <input type="checkbox" name="dat-pvalue" value="dat1p_v_N2.pvalue"> <label for="dat-pvalue"> pvalue </label><br>
                  <input type="checkbox" name="dat-padj" value="dat1p_v_N2.padj"> <label for="dat-padj"> padj </label><br>
                  <h3><i>rab-3p:</i><h3>
                  <input type="checkbox" name="rab-baseMean" value="rab3p_v_N2.baseMean"> <label for="rab-baseMean"> baseMean </label><br>
                  <input type="checkbox" name="rab-log2FoldChange" value="rab3p_v_N2.log2FoldChange"> <label for="rab-log2FoldChange"> log2FoldChange </label><br>
                  <input type="checkbox" name="rab-lfcSE" value="rab3p_v_N2.lfcSE"> <label for="rab-lfcSE"> lfcSE </label><br>
                  <input type="checkbox" name="rab-stat" value="rab3p_v_N2.stat"> <label for="rab-stat"> stat </label><br>
                  <input type="checkbox" name="rab-pvalue" value="rab3p_v_N2.pvalue"> <label for="rab-pvalue"> pvalue </label><br>
                  <input type="checkbox" name="rab-padj" value="rab3p_v_N2.padj"> <label for="rab-padj"> padj </label><br>
                  <h3><i>tph-1p & dat-1p:</i><h3>
                  <input type="checkbox" name="dt-baseMean" value="dat1p_tph1p_v_N2.baseMean"> <label for="dt-baseMean"> baseMean </label><br>
                  <input type="checkbox" name="dt-log2FoldChange" value="dat1p_tph1p_v_N2.log2FoldChange"> <label for="dt-log2FoldChange"> log2FoldChange </label><br>
                  <input type="checkbox" name="dt-lfcSE" value="dat1p_tph1p_v_N2.lfcSE"> <label for="dt-lfcSE"> lfcSE </label><br>
                  <input type="checkbox" name="dt-stat" value="dat1p_tph1p_v_N2.stat"> <label for="dt-stat"> stat </label><br>
                  <input type="checkbox" name="dt-pvalue" value="dat1p_tph1p_v_N2.pvalue"> <label for="dt-pvalue"> pvalue </label><br>
                  <input type="checkbox" name="dt-padj" value="dat1p_tph1p_v_N2.padj"> <label for="dt-padj"> padj </label><br>
                  genes:<br>
                  <textarea name="genes"></textarea>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == "__main__":        # on running python app.py
      app.run(debug=True)