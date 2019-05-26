from flask import Flask
from flask import render_template
from flask import request,redirect, url_for ,json
from flask import make_response, jsonify

import yaml

from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run()
