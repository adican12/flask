from flask import Flask
from flask import render_template
from mysql as mysql

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html',name=name)


@app.route('/mysql')
def mysql():
    print "start mysql"
    return mysql.connect()


if __name__ == '__main__':
  app.run()
