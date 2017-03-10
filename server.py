import json
from flask import Flask, request, render_template, url_for
from interface import Interface
app = Flask(__name__)

_interface = Interface()
_interface.query('machine learning')

@app.route("/")
def welcome():
    return render_template('index.html')


@app.route("/query", methods=['POST'])
def query():
    assert request.method == 'POST'
    query_str = request.form['inputValue']
    return json.dumps(_interface.query(query_str))


if __name__ == "__main__":
    app.run()