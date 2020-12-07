from flask import Flask           # import flask
from flask import render_template
from flask import request
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

        return '''{}'''.format(result)

    return '''<form method="POST">
                  dataseset:<br>
                  <input type="checkbox" name="tph" value="tph1p_v_N2"> <label for="tph"> tph-1p </label><br>
                  <input type="checkbox" name="dat" value="dat1p_v_N2"> <label for="tph"> dat-1p </label><br>
                  <input type="checkbox" name="tph" value="rab3p_v_N2"> <label for="tph"> rab-3p </label><br>
                  genes:<br>
                  <textarea name="genes"></textarea>
                  <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == "__main__":        # on running python app.py
      app.run(debug=True)