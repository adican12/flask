
from flask import Flask, render_template, send_file, request, session, redirect, url_for,make_response, jsonify
from flask_mysqldb import MySQL
import yaml
import os
import json
#from google.cloud import storage
import sys
from pyfcm import FCMNotification

app = Flask(__name__)

path = os.path.join('.', os.path.dirname(__file__), 'database.yaml')
y=open(path)
db = yaml.load(y)
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql = MySQL(app)

@app.route('/push_user', methods=['GET', 'POST'])
def push_user():
    massage = None
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            # user_id = str(user_id)
            cur = mysql.connection.cursor()
            cur.execute("""SELECT * from ad WHERE adID in (SELECT adid FROM notification WHERE user_id = {})""".format(user_id))
            rows = cur.fetchone()
            if rows:
                return jsonify({"status":"true" , "data":rows})
            else:
                return jsonify({"status":"true" , "data":rows ,"massage":"row is empty"})
        except Exception as e:
            return jsonify({"status": "false", "message": "get ads FAILS!", "Exception":str(e),"user_id":user_id})
    else:
        return render_template('push_user.html',error=massage)


@app.route('/get_coupnon', methods=['GET', 'POST'])
def get_coupnon():
    massage = None
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            user_id = int(user_id)
            cur = mysql.connection.cursor()
            cur.execute("""SELECT * from coupon WHERE couponID in (SELECT coupon_id FROM users_coupon WHERE user_id = {})""".format(user_id))

            rows = cur.fetchall()

            if rows:
                return jsonify({"status":"true" , "data":rows})
            else:
                return jsonify({"status":"true" , "data":rows ,"massage":"row is empty"})
        except Exception as e:
            return jsonify({"status": "false", "message": "get coupon FAILS!", "Exception":str(e)})
    else:
        return render_template('get_coupnon.html',error=massage)

@app.route('/get_ads', methods=['GET', 'POST'])
def get_ads():
    massage = None
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            # user_id = str(user_id)
            cur = mysql.connection.cursor()
            cur.execute("""SELECT * from ad WHERE adID in (SELECT adid FROM notification WHERE user_id = {})""".format(user_id))
            rows = cur.fetchall()
            if rows:
                return jsonify({"status":"true" , "data":rows})
            else:
                return jsonify({"status":"true" , "data":rows ,"massage":"row is empty"})
        except Exception as e:
            return jsonify({"status": "false", "message": "get ads FAILS!", "Exception":str(e),"user_id":user_id})
    else:
        return render_template('get_ads.html',error=massage)

def push_notf(token_device):
    try:
        push_service = FCMNotification(api_key="AAAABw6N4YM:APA91bFtQ2a3nky1IkOwF0BNBH0DVUTV4Hr6U7s0FKYkUFRMQ_0P8zpckqgQprBTEjjylmQYH898D533iW5-dUk1xFfP_xkz1c_vpmQcqfx1jU_bjuTjhkrV0vih-H6GsSZPh9nrPD0A")
        # OR initialize with proxies
        proxy_dict = {
              "http"  : "http://127.0.0.1",
            }
        registration_id = token_device
        # registration_id = "fBAt-6vVxt0:APA91bGUo8K6BYKm3tdyjD90xR6pp7D1mC8RaivskNJVUcPh5tqVRJouZeCc76IxRJdRf3HXASAMOmbI_pxVwAZrlGiKTL3wLQgN3dSx_sE4muuyZoFaRGjPQgB7j2f-1JD9Stzfa6Z4"
        message_title = "Cantor the cat"
        message_body = "Hope you're remmber to go out with ligal tonight"
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    # push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
    except:
        print("push_notf not working", result)

def handle_token(user_id,token):
    cur = mysql.connection.cursor()
    cond_query = "SELECT * FROM `devices` WHERE user_id={}".format(user_id)
    cur.execute(cond_query)
    row_count = cur.rowcount
    if row_count == 0 :
        qry1 = 'INSERT INTO `devices`(`user_id`, `token` ) VALUES( %s , %s )'
        cur.execute(qry1, (user_id, token))
        mysql.connection.commit()
    else:
         sql = "UPDATE `devices` SET token = %s WHERE user_id = %s"
         val = (token, user_id)
         cur.execute(sql,val)
         mysql.connection.commit()

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    massage = None
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        token = request.form['token']
        cur = mysql.connection.cursor()
        qry='SELECT * FROM users WHERE email=%s  AND password =%s '
        cur.execute(qry, (username, password))
        rows = cur.fetchall()
        for row in rows:
            _id = row["user_id"]
            user_type = row["user_type"]

        if user_type == "standard_user":
            handle_token(_id, token)
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
            return jsonify({
            "status": "false",
            "message": "not standard_user !"})

    else:
        return render_template('login.html',error=massage)


@app.route('/signup',methods=['GET','POST'])
def sign_up():
    massage = None
    if request.method == 'POST':
        _name = request.form['name']
        # _name = "name"
        _email = request.form['email']
        # _email = "email"
        _password = request.form['password']
        # _password = "password"
        # _birthday='2019-2-5'
        _birthday=request.form['birthday']
        _gender=request.form['gender']
        # _gender="gender"
        _phone=request.form['phone']
        # _mobile="phone"
        _user_type="standard_user"
        _category=request.form['category']
        # _user_category="category"
        _image=request.form['image']
        # _image="image"
        _status=0
        # return jsonify({"status": "true","name":_name,"email":_email,"password":_password,"birthday":_birthday,"gender":_gender,"phone":_phone,"category":_category,"image":_image})
        try:
            cur = mysql.connection.cursor()
            qry='INSERT INTO `users`( `name`, `email`, `password`, `gender`, `mobile`, `user_type`, `image`, `birthday`, `status`, `user_category`) VALUES( %s , %s , %s , %s , %s , %s , %s , %s , %s , %s)'
            cur.execute(qry,(_name  , _email , _password , _gender , _phone , _user_type , _image , _birthday , _status , _category ))
            mysql.connection.commit()
            return jsonify({"status": "true","message": "Data insert successfully!"})
        except Exception as e:
            return jsonify({"status": "false","message": "Data insert FAILS!"})
    else:
        return render_template('signup.html',error=massage)

@app.route('/feedback',methods=['GET','POST'])
def feedback():
    massage = None
    if request.method == 'POST':
        _user_id = request.form['user_id']
        # _user_id = "user_id"
        _ad_id = request.form['adID']
        # _ad_id = "adID"
        _rate = request.form['rate']
        try:
            cur = mysql.connection.cursor()
            qry='INSERT INTO `feedback`( `adID`,`user_id`,`rate`) VALUES( %s , %s , %s )'
            cur.execute(qry,(_user_id , _ad_id , _rate))
            mysql.connection.commit()
            return jsonify({"status": "true","message": "Data insert feedback successfully!"})
        except Exception as e:
            return jsonify({"status": "false","message": "Data insert feedback FAILS!"})
    else:
        return render_template('feedback.html',error=massage)
#
# @app.route('/users/<user_id>')
# def page(user_id):
#     # print(user_id)
#     cur = mysql.connection.cursor()
#     cur.execute("""SELECT * FROM users WHERE user_id = {}""".format(user_id))
#     rows = cur.fetchall()
#     return jsonify(rows)
#
# @app.route('/notf/<user_id>',methods=['GET'])
# def notf_user(user_id):
#     # print(user_id)
#     cur = mysql.connection.cursor()
#     cur.execute("""SELECT * FROM `notification` WHERE user_id = {}""".format(user_id))
#     rows = cur.fetchall()
#     return jsonify(rows)
#
# @app.route('/coupon/<user_id>',methods=['GET'])
# def coupon_user(user_id):
#     # print(user_id)
#     cur = mysql.connection.cursor()
#     cur.execute("""SELECT * FROM `users_coupon` WHERE user_id = {}""".format(user_id))
#     rows = cur.fetchall()
#     return jsonify(rows)
#

@app.route('/send_coupon/<_location_id>',methods=['GET','POST'])
def send_coupon(_location_id):
  try:
    cur = mysql.connection.cursor()
    qry = 'SELECT * FROM `users` WHERE location_id ={}'.format(_location_id)
    cur.execute(qry)
    rows = cur.fetchall()
    qry1 = 'SELECT * FROM `locations` WHERE locationID ={}'.format(_location_id)
    cur.execute(qry1)
    rows1 = cur.fetchall()
    for r1 in rows1:
        _business = r1["businessID"]
        qry2 = 'SELECT * FROM `coupon` WHERE busID ={}'.format(_business)
        cur.execute(qry2)
        rows2 = cur.fetchall()
        for r in rows:
            _user_id = r["user_id"]
            for r2 in rows2:
                _coupon_id = r2["couponID"]
                qry3 = 'INSERT INTO `users_coupon`( `user_id`, `coupon_id`,`counter`) VALUES( %s , %s ,%s )'
                cur.execute(qry3, (_user_id,_coupon_id ,0 ))
                mysql.connection.commit()
    return jsonify({
        "status": "true",
        "message": "Data fetched successfully!",
        "data": "update"})
  except Exception as e:
      return jsonify({"status": "false", "message": "Data insert coupon FAILS!"})
  finally:
      cur.close()

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
    #
    # print("Python version")
    # print (sys.version)
    # print("Version info.")
    # print (sys.version_info)
    # v= str(sys.version)
    # x=str(sys.version_info)
    # return jsonify({"python v":v,
    #                 "version info":x})
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


#count the number of users
def count_row_users():
    try:
        cur = mysql.connection.cursor()
        sql = 'SELECT * FROM users'
        cur.execute(sql)
        num_of_row = cur.rowcount
        cur.execute(sql)
        # result = cur.fetchall()
        # print(result)
        return num_of_row
    except:
        return render_template("welcome.html", massage="count raw doesnt work")
    finally:
        cur.close()

#des: function that get in order to start process match user to campian
#@app.route('/run1',methods=['GET','POST'])
def run_campaign(num):
    try:
     cur = mysql.connection.cursor()
     qry = 'SELECT * FROM users WHERE user_id = {} '.format(num)
     cur.execute(qry)
     rows = cur.fetchall()
     for r in rows:
        id = r["user_id"]
        user_category = r["user_category"]
        location_id = r["location_id"]
        status_user = r["status"]
        # if location_id == "NULL":
        #    break
        return id ,user_category ,location_id , status_user
    except:
        return render_template("welcome.html", massage="run campaign doesnt work")
    finally:
        cur.close()


def ad_match_to_user(user_id ,user_category , _location_id):
  try:
    cur = mysql.connection.cursor()
    qry = 'SELECT * FROM `campaign` WHERE locationID ={}'.format(_location_id)
    cur.execute(qry)
    rows = cur.fetchall()
    if len(rows)==0 : #TODO
        qry_defualt_2 = 'SELECT * FROM `campaign` WHERE locationID ={}'.format(_location_id)
        cur.execute(qry_defualt_2)
        rows = cur.fetchall()
    list_of_info_of_campaign = []
    list_of_matched_user_and_ad = []
    for row in rows:
         loc_id = row["locationID"]
         category = row["category"]
         ad_id = row["adID"]
         info_of_ad=(loc_id , category , ad_id)
         list_of_info_of_campaign.append(info_of_ad)
    for match_item in list_of_info_of_campaign:
        if match_item[1] == user_category:
            matched_obj=(match_item[2] ,user_id)
            list_of_matched_user_and_ad.append(matched_obj)
        else: #TODO
            defulat_ad = 'SELECT * FROM `ad` WHERE adID ={}'.format(2)
            print("check not match")
            cur.execute(defulat_ad)
            defualt_ad = cur.fetchone()
            print("level-1")
            for var in defualt_ad:
                ad_id_defult = defualt_ad["adID"]
            matched_obj = (ad_id_defult, user_id)
            list_of_matched_user_and_ad.append(matched_obj)
            print("level-2")
    return list_of_matched_user_and_ad
  except:
      return render_template("welcome.html", massage="ad matching doesnt work")
  finally:
      cur.close()

def insert_notf_to_db(list_of_matched):
  try:
    cur = mysql.connection.cursor()
    for item in list_of_matched:
        cond_query = "SELECT * FROM `notification` WHERE user_id={} AND  adid={}".format(item[1],item[0])
        print("insert db problem")
        cur.execute(cond_query)
        notf_= cur.fetchone()
        row_count = cur.rowcount
    # print(row_count)
    if row_count == 0 :
        qry = 'INSERT INTO `notification`( `adid`, `user_id`) VALUES( %s , %s )'
        cur.execute(qry,(item[0], item[1]))
        mysql.connection.commit()
    return render_template("welcome.html", massage="add notf success")
  except:
      return render_template("welcome.html", massage="add notf doesnt success")
  finally:
      cur.close()

@app.route('/init',methods=['GET','POST'])
def init_run():
    try:
        num_of_row = count_row_users()
        num_of_row =num_of_row
        for i in range(1,num_of_row+1):
         print(i)
         id_user,user_category,location_id ,status= run_campaign(i)
         if status ==1:
            result = "result1: " + str(id_user) + " , result2: " + str(user_category) + " , result3: " + str(location_id)
            match_list_of_users = ad_match_to_user(id_user , user_category , location_id )
            print("after ad match")
            insert_notf_to_db(match_list_of_users)
            print("after insert")
            result=push_notification(i)
            print(result)
         elif status == 0:
             pass
        return render_template("welcome.html", massage = match_list_of_users)
    except:
      return render_template("welcome.html", massage="init_run_problem")


@app.route('/push/<index_token>',methods=['GET','POST'])
def push_notification(user_id):
    try:
        cur = mysql.connection.cursor()
        qry = 'SELECT * FROM `devices` WHERE user_id ={}'.format(user_id)
        cur.execute(qry)
        rows = cur.fetchall()
        for row in rows:
            _token=row["token"]
        push_notf(_token)

        return jsonify({"status": "true",
        "message": "Data fetched successfully!",
        "data": "result"})
    except:
        return render_template("welcome.html", massage="push main problem")


# def bring_user_id_form_notf(user_id_app):
#  try:
#      cur = mysql.connection.cursor()
#      qry = 'SELECT * FROM `notification` WHERE user_id = {} '.format(user_id_app)
#      cur.execute(qry)
#      rows = cur.fetchall()
#      if len(rows) ==1:
#       for items in rows:
#          not_id_app = items["noteid"]
#          ad_id_app = items["adid"]
#          ad_user_id_app = items["user_id"]
#       print(not_id_app,ad_id_app,ad_user_id_app)
#       return ad_id_app
#      else:
#          pass
#  except:
#      return render_template("welcome.html", massage="problem in push notification(adid)")
#  finally:
#     cur.close()


#
# def extract_image_from_ad_id(ad_id_app):
#     try:
#         cur = mysql.connection.cursor()
#         qry = 'SELECT * FROM `ad` WHERE adID = {} '.format(ad_id_app)
#         cur.execute(qry)
#         rows = cur.fetchall()
#         for items in rows:
#             app_image = items["image"]
#         return app_image
#     except:
#         return render_template("welcome.html", massage="image problem from extarct")
#     finally:
#         cur.close()

# main
if __name__ == '__main__':
    app.run(debug=True)
