import mysql.connector


def connect():
    mydb = mysql.connector.connect(
        host="10.164.0.3",
        user="root",
        passwd="1"
    )
    print(mydb)
