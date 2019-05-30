from flask import Flask, render_template, send_file, request, session, redirect, url_for,make_response, jsonify
from flask_mysqldb import MySQL
import yaml
import os
import json



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
        username = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        qry='SELECT * FROM users WHERE email=%s  AND password =%s '
        cur.execute(qry, (username, password))
        rows = cur.fetchall()
        if len(rows) > 0:
            return jsonify({
                    "status": "true",
                    "message": "Data fetched successfully!",
                    "data": rows,
                    "username":username,
                    "password":password})

        else:
            return jsonify({
            "status": "false",
            "message": "Data fetched fails!",
            "data": rows})
    else:
        return render_template('login.html',error=massage)

# @app.route('/showsignup')
# def showSignUp():
#    return render_template('signup.html')

@app.route('/signup',methods=['GET','POST'])
def sign_up():
    massage = None
    if request.method == 'POST':
        # form = request.form
        _name = request.form['name']
        # _name = "name"

        _email = request.form['email']
        # _email = "email"

        _password = request.form['password']
        # _password = "password"

        _birthday='2019-2-5'
        # _birthday=request.form['birthday']

        # _gender=request.form['gender']
        _gender="gender"

        # _mobile=request.form['phone']
        _mobile="phone"

        _user_type="standard_user"

        # _user_category=request.form['category']
        _user_category="category"

        # _image=request.form['image']
        _image="image"

        _status=0
        return jsonify({"status": "true",
                        "_name":_name,
                        "_email":_email,
                        "_password":_password,
                        "_gender":_gender,
                        "_mobile":_mobile
                        })



        # cur = mysql.connection.cursor()
        # qry='INSERT INTO `users`( `name`, `email`, `password`, `gender`, `mobile`, `user_type`, `image`, `birthday`, `status`, `user_category`) VALUES( %s , %s , %s , %s , %s , %s , %s , %s , %s , %s)'
        # cur.execute(qry, (_name , _email , _password , _gender , _mobile , _user_type , _image , _birthday , _status , _user_category ))
        # mysql.connection.commit()

        # return jsonify({"status": "true","message": "Data insert successfully!"})
    else:
        return render_template('signup.html',error=massage)


@app.route('/users/<user_id>')
def page(user_id):
    # print(user_id)
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM users WHERE name = {}""".format(user_id))
    rows = cur.fetchall()
    return jsonify(rows)


@app.route('/')
def index():
    return render_template('index.html')

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




#
# try:
#   print(x)
# except:
#   print("Something went wrong")
# finally:
#   print("The 'try except' is finished")




#des: function that get in order to start process match user to campian
#@app.route('/run1',methods=['GET','POST'])
def run_campaign():
    try:
     cur = mysql.connection.cursor()
     qry = 'SELECT * FROM users WHERE id = 1 '
     cur.execute(qry)
     rows = cur.fetchall()
     for r in rows:
        id= r["id"]
        user_category=r["user_category"]
        location_id=r["location_id"]

     return id ,user_category ,location_id
    except:
        print("error")
    finally:
        cur.close()


def ad_match_to_user(user_id ,user_category , _location_id):
    cur = mysql.connection.cursor()
    qry = 'SELECT * FROM `campaign` WHERE location_id ={}'.format(_location_id)
    cur.execute(qry)
    rows = cur.fetchall()
    list_of_info_of_campaign = []
    list_of_matched_user_and_ad = []
    for row in rows:
         loc_id = row["location_id"]
         category = row["category"]
         ad_id = row["adID"]
         info_of_ad=(loc_id , category , ad_id)
         list_of_info_of_campaign.append(info_of_ad)
    for match_item in list_of_info_of_campaign:
        if match_item[1] == user_category:
            matched_obj=(match_item[2] ,user_id)
            list_of_matched_user_and_ad.append(matched_obj)
        else:
            #bring another adv from general table
            pass
    return list_of_matched_user_and_ad



def insert_notf_to_db(list_of_matched):

    cur = mysql.connection.cursor()
    for item in list_of_matched:
        cond_query = "SELECT * FROM `notification` WHERE user_id={} AND  adid={}".format(item[1],item[0])
        cur.execute(cond_query)
        row_count = cur.rowcount
    # print(row_count)
    if row_count == 0:
        qry = 'INSERT INTO `notification`( `adid`, `user_id`) VALUES( %s , %s )'
        cur.execute(qry,(item[0], item[1]))
        mysql.connection.commit()




@app.route('/init',methods=['GET','POST'])
def init_run():

    id_user,user_category,location_id = run_campaign()
    result = "result1: " + str(id_user) + " , result2: " + str(user_category) + " , result3: " + str(location_id)
    match_list_of_users = ad_match_to_user(id_user , user_category , location_id )
    insert_notf_to_db(match_list_of_users)

    return render_template("welcome.html",massage = match_list_of_users)


# main
if __name__ == '__main__':
    app.run(debug=True)
