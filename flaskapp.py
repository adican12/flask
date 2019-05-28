from flask import Flask, render_template, send_file, request, session, redirect, url_for,make_response, jsonify
from flask_mysqldb import MySQL
import yaml
import os

app = Flask(__name__)

path = os.path.join('.', os.path.dirname(__file__), 'db.yaml')
y=open(path)
db = yaml.load(y)
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql = MySQL(app)



# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    massage = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cur = mysql.connection.cursor()
            cur.execute("""SELECT * FROM users WHERE name = {}""".format(username))
            rows = cur.fetchall()

            if rows > 0:
                return jsonify({
                        "status": "true",
                        "message": "Data fetched successfully!",
                        "data": rows})

            else:
                return jsonify({
                "status": "false",
                "message": "Data fetched fails!",
                "data": rows})

        except Exception as e:
                return jsonify({
                "status": "false",
                "message": "Data fetched fails!",
                "data": e})

    else:
        return render_template('login.html',error=massage)

@app.route('/showsignup')
def showSignUp():
   return render_template('signup.html')

@app.route('/signup',methods=['GET','POST'])
def sign_up():
    # read the posted values from the UI
    form = request.form
    _name=request.form['username']
    _password=request.form['password']
    _email=request.form['email']
    _gender=request.form['gender']
    _phone=request.form['mobile']
    _birthday=request.form['birthday']
    _image=request.form['image']

    if _name and _password and _email and _gender and _phone and _birthday and _image:
        try:
            cur = mysql.connection.cursor()
            result  = cur.execute('INSERT INTO users( name , email , password ,gender , mobile , user_type , image , birthday , status , user_category ) VALUES ( %s , %s , %s , %s , %s ,"standard_user", %s , %s , 1 ,"love")',(_name,_email,_password,_gender,_phone,_birthday,_image))
            mysql.connection.commit()
        except Exception as e:
            return json.dumps({'message': 'User created successfully !'})
        else:
            return json.dumps({'error': str(data[0])})

    else:
         return json.dumps({'html': '<span>Enter the required fields</span>'})


@app.route('/users/<user_id>')
def page(user_id):
    # print(user_id)
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM users WHERE name = {}""".format(user_id))
    rows = cur.fetchall()
    return jsonify(rows)


@app.route('/users',methods=["GET"])
def users():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM users")
    if result_value > 0:
        users = cur.fetchall()
    return jsonify({
    "status": "true",
    "message": "Data fetched successfully!",
    "data": users})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    massage = "welcome str"
    return render_template('welcome.html',massage=massage)

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
    app.run(debug=True)
