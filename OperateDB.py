import pymysql
from pymongo import *


userId=[]
userId2=[]
def get_userid_form_Mysql():
    con=pymysql.connect(host='127.0.0.1',user='root',passwd='123456',db='app_back')
    cursor = con.cursor()
    sql = "select userId from user WHERE ISNULL(isAuth) and inviteCode!=''"
    cursor.execute(sql)
    row = cursor.fetchall()
    for id in row:
        print(id[0])
        userId.append(id[0])
    cursor.close()
    con.close()

def modify_mongodb_for_useid():
    #client = MongoClient("mongodb://{}:{}@{}:{}"
                                     # .format(MONGO_USER,
                                      #        MONGO_PASS,
                                       #       MONGO_HOST,
                                        #      MONGO_PORT))
    client = MongoClient(host="localhost", port=27017)
    mydb = client["stocks"]
    count=0
    Acount = 0
    for id in userId:
        my_set = mydb["stock"]
        Acount += 1
        myquery = {"userId": id}
        mydoc = my_set.find({"userId": id,"income":{"$ne": 0}})
        #mydoc = my_set.find(myquery)
        for x in mydoc:
            print(x)
            count+=1
            print(count)
            newvalues = {"$set": {"income": 0}}
            my_set.update(myquery, newvalues)
    print("userId Acount %d,Modify count %d"  % (Acount,count))
    client.close()

def get_mongodb_for_useid():
    client = MongoClient(host="localhost", port=27017)
    mydb = client["stocks"]
    my_set = mydb["stock"]
    for x in my_set.find():
        userId2.append(x['userId'])
    print(userId2)
    print(len(userId2))

def rec_userid_form_Mysql():
    con=pymysql.connect(host='127.0.0.1',user='root',passwd='123456',db='app_back')
    for id in userId2:
        cursor = con.cursor()
        sql = "select isAuth from user WHERE userId='%s'"%(id)
        #sql = "select name from user_auth WHERE user_id='%s'" %(id)
        cursor.execute(sql)
        row = cursor.fetchall()
        for idd in row:
            print("userId = %s,isAuth=%s"%(id,idd[0]))
            userId.append(idd[0])
    cursor.close()
    con.close()

'''
    Get data from the mysql, modify mongodb
        get_userid_form_Mysql()
        modify_mongodb_for_useid()
        
    Get data from the mongodb, modify mysql
        get_mongodb_for_useid()
        rec_userid_form_Mysql()
'''
if __name__ == '__main__':
    get_userid_form_Mysql()
    print(userId)
    print("userId Acount %d" % (len(userId)))
    modify_mongodb_for_useid()
    #get_mongodb_for_useid()
    #rec_userid_form_Mysql()