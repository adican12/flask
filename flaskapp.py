from flask import Flask, render_template, send_file, request, session, redirect, url_for,make_response
from flask_mysqldb import MySQL
import yaml
import os

app = Flask(__name__)

f= open("log.txt","w+")
for i in range(10):
     f.write("This is line %d\r\n" % (i+1))
     

# db = yaml.load(open('db.yaml'),Loader=yaml.FullLoader)
# app.config['MYSQL_HOST']=db['mysql_host']
# app.config['MYSQL_USER']=db['mysql_user']
# app.config['MYSQL_PASSWORD']=db['mysql_password']
# app.config['MYSQL_DB']=db['mysql_db']
# app.config['MYSQL_CURSORCLASS']='DictCursor'
# mysql = MySQL(app)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            # return redirect(url_for('home'))
            return render_template('/welcome.html')
    return render_template('login.html', error=error)

@app.route('/showsignup')
def showSignUp():
   return render_template('signup.html')

@app.route('/signup',methods=['GET','POST'])
def sign_up():
    # read the posted values from the UI
    #try:
    form = request.form
    _name=request.form['username']
    _password=request.form['password']
    _email=request.form['email']
    _gender=request.form['gender']
    _phone=request.form['mobile']
    _birthday=request.form['birthday']
    _image=request.form['image']
    return render_template('signup.html')
        #
        # if _name and _password and _email and _gender and _phone and _birthday and _image:
        #     # cur = mysql.connection.cursor()
        #     #
        #     # _hashed_password = generate_password_hash(_password)
        #     # cur.execute('INSERT INTO users( name , email , password ,gender , mobile , birthday ,image ) VALUES (%s,%s,%s,%s,%s,%s,%s)',(_name,_email,_password,_gender,_phone,_birthday,_image))
        #     # data = cur.fetchall()
        #     #
        #     # if len(data) is 0:
        #     #     mysql.connection.commit()
        #     #     return json.dumps({'message': 'User created successfully !'})
        #     # else:
        #     #     return json.dumps({'error': str(data[0])})
        # else:
        #      return json.dumps({'html': '<span>Enter the required fields</span>'})

    # except Exception as e:
    #     return json.dumps({'error': str(e)})
    # finally:
    #     cur.close()




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
