import MySQLdb

#
# def catifi_connect():
#  mydb = MySQLdb.connect(
#   host="localhost",
#   user="cat",
#   passwd="catwifi808" ,
#   database = "catifi"
#  )
#  #show DB tables
#  mycursor = mydb.cursor()
#  mycursor.execute("SHOW TABLES")
#  for x in mycursor:
#      print(x)
#  return mydb



def run_campaign(mydb):
  mycursor = mydb.cursor()
  sql = "SELECT * FROM campaign WHERE location_id = 1"

  mycursor.execute(sql)
  myresult = mycursor.fetchall()

  #x=row
  for x in myresult:
    #print(x)
    print("campaignID ={},".format(x[0]),"campaignName = ,".format(x[1]),"id  = {},".format(x[2]),"adID  = {},".format(x[3]),"gender  = {},".format(x[4]),"ageMin = {}, ".format(x[5])
          , "ageMax ={}, ".format(x[6]), "budget  ={} ,".format(x[7]), "category  ={} ,".format(x[8]),
          "startingDate = {},".format(x[9]), "endDate = {},".format(x[10]))
    print("location_id  ={}.".format(x[11]), "\n")
    return x[11] , x[8] ,x[3]


def all_users_in_specific_router_location(location_id):
  mycursor = mydb.cursor()
  sql = "SELECT * FROM locations WHERE location_id = {}".format(location_id)
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  list_of_id_user = []
  for rows in myresult:
      print("locationId:={},".format(rows[0]), "lat:{},".format(rows[1]), "lng:{},".format(rows[2]),"info:{},".format(rows[3]), "description:{},".format(rows[4]), "userId:{}.".format(rows[5]))
      list_of_id_user.append(rows[5])
  #in this point we are returned a list of the users in specspic location
  for i in list_of_id_user:
      if i == "":
          list_of_id_user.remove(i)
  return list_of_id_user




def match_user_from_location_router(list_of_id_user):
    mycursor = mydb.cursor()

    print(list_of_id_user)
    list_of_id_and_category = []
    for i in list_of_id_user:
     sql = "SELECT * FROM users WHERE id = {}".format(i)
     mycursor.execute(sql)
     myresult = mycursor.fetchall()
     #print(myresult)
     for rows in myresult:
         print("id:={},".format(rows[0]),"name:={},".format(rows[1]), "email:{},".format(rows[2]), "password:{},".format(rows[3]),
               "gender:{},".format(rows[4]), "mobile:{},".format(rows[5]), "userType:{}.".format(rows[6]),"image:{}.".format(rows[7]),"birthday:{}.".format(rows[8]),"status:{}.".format(rows[9]),"category:{}.".format(rows[10]),"location_id:{}.".format(rows[11]))
         users_id_and_category=(rows[0],rows[10])
     list_of_id_and_category.append(users_id_and_category)
    return list_of_id_and_category


def match_adv_to_user(ad_id,id_user):
    print("####")
    mycursor = mydb.cursor()
    ##add check for exsist id
    print(ad_id,id_user)
    cond_query ="SELECT id FROM notification WHERE id".format(id_user)
    mycursor.execute(cond_query)
    row_count = mycursor.rowcount
    #print(row_count)
    if row_count == 0:
        #print("row_count:",row_count)
        sql = "INSERT INTO notification (id, adID) VALUES (%s, %s)"
        val = (id_user, ad_id)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Done")
    elif row_count == 1:
        print("exist")
    elif row_count > 1 :
        print("exist")


def init_run(mydb):
    location_id_returned_value, category_id_returned_value, ad_id_returned_value = run_campaign(db_catwifi)
    print("####")
    print("location_id: ,", location_id_returned_value, "category: ", category_id_returned_value)
    users_id = all_users_in_specific_router_location(location_id_returned_value, db_catwifi)
    # print(users_id)
    list_users_info = match_user_from_location_router(users_id, db_catwifi)
    for j in list_users_info:
        if j[1] != category_id_returned_value:
            pass
        else:
            result_categorey_id = j[0]
    print("Category result id: ", result_categorey_id)
    match_adv_to_user(ad_id_returned_value, result_categorey_id, db_catwifi)



#
# if __name__== "__main__":
#   db_catwifi = catifi_connect()
#   init_run(db_catwifi)