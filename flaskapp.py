from flask import Flask
from flask import render_template
from flask import request,redirect, url_for ,json

# from mysql as mysql
# import logging


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html',name=name)


# @app.route('/mysql')
# def mysql():
#     print('start mysql', file=sys.stderr)
#     app.logger.warning('testing warning log')
#     app.logger.error('testing error log')
#     app.logger.info('testing info log')
#     mysql.connect()


if __name__ == '__main__':
  app.run()
