from flask import Flask, render_template, send_file, request, session, redirect, url_for,make_response

# from flask_mysqldb import MySQL
#
# import yaml

app = Flask(__name__)




@app.route('/showsignup')
def showSignUp():
   return render_template('signup.html')




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

#cookie response
@app.route('/cookie')
def coockie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

#error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# main
if __name__ == '__main__':
    app.run()
