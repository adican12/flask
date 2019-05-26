from flask import Flask
from flask import render_template
from flask import request,redirect, url_for ,json
from flask import make_response, jsonify

import yaml

# from flask_mysqldb import MySQL

app = Flask(__name__)

#Configure db
# db = yaml.load(open('C:\\Users\\yarde\\PycharmProjects\\Backendv1\\db.yaml'),Loader=yaml.FullLoader)
# app.config['MYSQL_HOST']=db['mysql_host']
# app.config['MYSQL_USER']=db['mysql_user']
# app.config['MYSQL_PASSWORD']=db['mysql_password']
# app.config['MYSQL_DB']=db['mysql_db']
# app.config['MYSQL_CURSORCLASS']='DictCursor'
# mysql = MySQL(app)



@app.route('/')
def home():
    return "<p>Your browser is %s</p>"

    #conn = db_connect.connect()  # connect to database
    #cur = mysql.connection.cursor()
    #cur.execute('INSERT INTO user( name , age ) VALUES (%s,%s)',('yarden','26'))
    #mysql.connection.commit()


    # user_agent = request.headers.get('User-Agent')
    # return '<p>Your browser is %s</p>' % user_agent

    # ------------------------------------------return for check------------------------------------------

# @app.route('/signup',methods=['GET','POST'])
# def sign_up():
    # read the posted values from the UI
    #try:
        # form = request.form
        # _name=request.form['username']
        # _password=request.form['password']
        # _email=request.form['email']
        # _gender=request.form['gender']
        # _phone=request.form['mobile']
        # _birthday=request.form['birthday']
        # _image=request.form['image']
        # if _name and _password and _email and _gender and _phone and _birthday and _image:
        #     cur = mysql.connection.cursor()
        #
        #     _hashed_password = _password
        #     cur.execute('INSERT INTO users( name , email , password ,gender , mobile , birthday ,image ) VALUES (%s,%s,%s,%s,%s,%s,%s)',(_name,_email,_password,_gender,_phone,_birthday,_image))
        #     data = cur.fetchall()
        #
        #     if len(data) is 0:
        #         mysql.connection.commit()
        #         return json.dumps({'message': 'User created successfully !'})
        #     else:
        #         return json.dumps({'error': str(data[0])})
        # else:
        #      return json.dumps({'html': '<span>Enter the required fields</span>'})

    # except Exception as e:
    #     return json.dumps({'error': str(e)})
    # finally:
    #     cur.close()

#     # ------------------------------------------return for check------------------------------------------
#     return "sign_up"
#
# @app.route('/showsignup')
# def showSignUp():
#    return render_template('signup.html')
#
#
# @app.route('/users',methods=["GET"])
# def users():
#     # cur = mysql.connection.cursor()
#     # result_value = cur.execute("SELECT * FROM users")
#     # print(result_value)
#     # if result_value > 0:
#     #     users = cur.fetchall()
#
#
#         #print(users)
#        #return users[0]
#
#
#     # return jsonify(users)
#
#     # ------------------------------------------return for check------------------------------------------
#     return "<p>users</p>"
#
#
#
# @app.route('/welcome')
# def welcome():
#     return render_template('welcome.html')
#
#
#
# #cookie response
# @app.route('/cookie')
# def coockie():
#     # response = make_response('<h1>This document carries a cookie!</h1>')
#     # response.set_cookie('answer', '42')
#     # return response
#
#     # ------------------------------------------return for check------------------------------------------
#     return "<p>cookie</p>"
#
#
#
#
#
# # Route for handling the login page logic
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # error = None
#     # if request.method == 'POST':
#     #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#     #         error = 'Invalid Credentials. Please try again.'
#     #     else:
#     #         return redirect(url_for('home'))
#     # return render_template('login.html', error=error)
#
#
#     # ------------------------------------------return for check------------------------------------------
#     return "<p>login</p>"
#
#
# @app.route('/users/<user_id>')
# def page(user_id):
#     # print(user_id)
#     # cur = mysql.connection.cursor()
#     # cur.execute("""SELECT * FROM users WHERE name = {}""".format(user_id))
#     # rows = cur.fetchall()
#     # print(rows)
#     # #for row in rows:
#     # return jsonify(rows)
#
#
#     # ------------------------------------------return for check------------------------------------------
#     return "<p>users</p>"



#error handler
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500
#
#



if __name__ == '__main__':
    app.run(debug=True)
