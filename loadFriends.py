import json
import re

import db
def loadData():
    conn = db.dbConnection()
    print("Started Reading user JSON file which contains multiple JSON document")
    #Creating a cursor object using the cursor() method    
    cursor = conn.cursor()
    data = []
    with open('yelp_user.json') as f: 
        for jsonObj in f:
            dict = json.loads(jsonObj)            
            if(len(dict) > 0):             
                frd = dict['friends']
                if (len(frd) > 0):
                    for fd in frd:
                        data.append(dict['user_id'])
                        data.append(fd)
                        sql = """
                            INSERT INTO friends ( user_id, friend_id)
                                VALUES ( %(user_id)s, %(friend_id)s)
                        """                      
                        cursor.execute(sql, {                    
                            'user_id': data[0],
                            'friend_id': data[1]
                        }) 
                        conn.commit()
                        data.clear()
                print("List has been inserted to friends table successfully...")
        conn.close()
