import json
import re

import db
def loadData():
    conn = db.dbConnection()
    print("Started Reading Review JSON file which contains multiple JSON document")
    #Creating a cursor object using the cursor() method    
    cursor = conn.cursor()
    data = []
    with open('yelp_review.json') as f: 
        
        for jsonObj in f:
            dict = json.loads(jsonObj)            
            if(len(dict) > 0):
                print(dict)
                data.append(dict['review_id'])
                data.append(dict['business_id'])
                data.append(dict['user_id'])
                data.append(dict['stars'])
                data.append(dict['date'])              
                data.append(dict['text'])
                data.append(dict['useful'])
                data.append(dict['funny'])
                data.append(dict['cool']) 
                sql = """
                    INSERT INTO review ( review_id, business_id, user_id, stars, date,text,useful,funny,cool)
                        VALUES ( %(review_id)s, %(business_id)s, %(user_id)s, %(stars)s, %(date)s, %(text)s, %(useful)s, %(funny)s, %(cool)s );
                """                      
                cursor.execute(sql, {
                    'review_id': data[0],
                    'business_id': data[1],
                    'user_id': data[2],
                    'stars': data[3],
                    'date': data[4],
                    'text': data[5],
                    'useful':str(data[6]),
                    'funny': str(data[7]),
                    'cool': str(data[8])
                }) 
                conn.commit()
                data.clear()
                print("List has been inserted to business hours table successfully...")
        conn.close()
def cleanStr4SQL(s):
    return s.replace("'","''").replace("\n"," ")
