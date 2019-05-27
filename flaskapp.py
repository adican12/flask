from flask import Flask, render_template, send_file, request, session, redirect, url_for,make_response

# from flask_mysqldb import MySQL
#
# import yaml

app = Flask(__name__)



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
        
        if _name and _password and _email and _gender and _phone and _birthday and _image:
            return render_template("welcome.html")
            # cur = mysql.connection.cursor()
            #
            # _hashed_password = generate_password_hash(_password)
            # cur.execute('INSERT INTO users( name , email , password ,gender , mobile , birthday ,image ) VALUES (%s,%s,%s,%s,%s,%s,%s)',(_name,_email,_password,_gender,_phone,_birthday,_image))
            # data = cur.fetchall()
            #
            # if len(data) is 0:
            #     mysql.connection.commit()
            #     return json.dumps({'message': 'User created successfully !'})
            # else:
            #     return json.dumps({'error': str(data[0])})
        else:
             return json.dumps({'html': '<span>Enter the required fields</span>'})

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
