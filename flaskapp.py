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

@app.route('/showsignup')
def showSignUp():
   return render_template('signup.html')




@app.route('/signup',methods=['POST'])
def sign_up():
    try:
        form = request.form
        _name=request.form['username']
        _email=request.form['email']
        _password=request.form['password']
        _gender=request.form['gender']
        _mobile=request.form['mobile']
        _user_type="standard_user"
        _image=request.form['image']
        # _birthday=request.form['birthday']
        _birthday='2019-2-5'
        _status=0
        _user_category="Demo"
        cur = mysql.connection.cursor()
        qry='INSERT INTO `users`( `name`, `email`, `password`, `gender`, `mobile`, `user_type`, `image`, `birthday`, `status`, `user_category`) VALUES( %s , %s , %s , %s , %s , %s , %s , %s , %s , %s)'
        cur.execute(qry, (_name , _email , _password , _gender , _mobile , _user_type , _image , _birthday , _status , _user_category ))
        mysql.connection.commit()

        return jsonify({
                    "status": "true",
                    "message": "Data insert successfully!"})
    except Exception as e:
        return jsonify({"status":"fails", "Exception":e})

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











#@app.route('/run1',methods=['GET','POST'])
def run_campaign():
  mycursor = mysql.connection.cursor()
  qry = 'SELECT * FROM ad WHERE adID = 1 '
  mycursor.execute(qry)
  myresult = mycursor.fetchall()
  #convert_tuple_to_str = json.dumps(myresult)
  #json_from_str = json.loads(convert_tuple_to_str)
  #json_result = json.dump(myresult)
  #json_vars = json.load(json_result)
  #for x in myresult:
  return myresult["adID"]
#
# def all_users_in_specific_router_location(location_id):
#   mycursor =  mysql.connection.cursor()
#   sql = "SELECT * FROM locations WHERE location_id = {}".format(location_id)
#   mycursor.execute(sql)
#   myresult = mycursor.fetchall()
#   list_of_id_user = []
#   for rows in myresult:
#       print("locationId:={},".format(rows[0]), "lat:{},".format(rows[1]), "lng:{},".format(rows[2]),"info:{},".format(rows[3]), "description:{},".format(rows[4]), "userId:{}.".format(rows[5]))
#       list_of_id_user.append(rows[5])
#   #in this point we are returned a list of the users in specspic location
#   for i in list_of_id_user:
#       if i == "":
#           list_of_id_user.remove(i)
#   return list_of_id_user
#
#
#
#
# def match_user_from_location_router(list_of_id_user):
#     mycursor =  mysql.connection.cursor()
#
#     print(list_of_id_user)
#     list_of_id_and_category = []
#     for i in list_of_id_user:
#      sql = "SELECT * FROM users WHERE id = {}".format(i)
#      mycursor.execute(sql)
#      myresult = mycursor.fetchall()
#      #print(myresult)
#      for rows in myresult:
#          print("id:={},".format(rows[0]),"name:={},".format(rows[1]), "email:{},".format(rows[2]), "password:{},".format(rows[3]),
#                "gender:{},".format(rows[4]), "mobile:{},".format(rows[5]), "userType:{}.".format(rows[6]),"image:{}.".format(rows[7]),"birthday:{}.".format(rows[8]),"status:{}.".format(rows[9]),"category:{}.".format(rows[10]),"location_id:{}.".format(rows[11]))
#          users_id_and_category=(rows[0],rows[10])
#      list_of_id_and_category.append(users_id_and_category)
#     return list_of_id_and_category
#
#
# def match_adv_to_user(ad_id,id_user):
#     print("####")
#     mycursor =  mysql.connection.cursor()
#     ##add check for exsist id
#     print(ad_id,id_user)
#     cond_query ="SELECT id FROM notification WHERE id".format(id_user)
#     mycursor.execute(cond_query)
#     row_count = mycursor.rowcount
#     #print(row_count)
#     if row_count == 0:
#         #print("row_count:",row_count)
#         sql = "INSERT INTO notification (id, adID) VALUES (%s, %s)"
#         val = (id_user, ad_id)
#         mycursor.execute(sql, val)
#         mysql.connection.commit()
#         print("Done")
#     elif row_count == 1:
#         print("exist")
#     elif row_count > 1 :
#         print("exist")


@app.route('/init',methods=['GET','POST'])
def init_run():
    result = run_campaign()

    #location_id_returned_value, category_id_returned_value, ad_id_returned_value = run_campaign()
    # print("####")
    # print("location_id: ,", location_id_returned_value, "category: ", category_id_returned_value)
    # users_id = all_users_in_specific_router_location(location_id_returned_value)
    # # print(users_id)
    # list_users_info = match_user_from_location_router(users_id)
    # for j in list_users_info:
    #     if j[1] != category_id_returned_value:
    #         pass
    #     else:
    #         result_categorey_id = j[0]
    # print("Category result id: ", result_categorey_id)
    # match_adv_to_user(ad_id_returned_value, result_categorey_id)
    return render_template("welcome.html",massage = type(result))


# main
if __name__ == '__main__':
    app.run(debug=True)
