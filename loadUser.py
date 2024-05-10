import json
import re

import db
def loadData():
    conn = db.dbConnection()
    print("Started Reading User JSON file which contains multiple JSON document")
    #Creating a cursor object using the cursor() method    
    cursor = conn.cursor()
    data = []
    with open('yelp_user.json') as f: 
        for jsonObj in f:
            dict = json.loads(jsonObj)            
            if(len(dict) > 0):
                print(dict)                
                data.append(dict['average_stars'])
                data.append(dict['compliment_cool'])
                data.append(dict['compliment_cute'])
                data.append(dict['compliment_funny'])
                data.append(dict['compliment_hot'])
                data.append(dict['compliment_list'])
                data.append(dict['compliment_more'])
                data.append(dict['compliment_note'])
                data.append(dict['compliment_photos'])
                data.append(dict['compliment_plain'])
                data.append(dict['compliment_profile'])
                data.append(dict['compliment_writer'])
                data.append(dict['cool'])
                data.append(dict['fans'])
                data.append(dict['funny'])
                data.append(dict['name'])
                data.append(dict['review_count'])
                data.append(dict['useful'])
                data.append(dict['user_id'])
                data.append(dict['yelping_since'])
                sql = """
                    INSERT INTO users ( average_stars, compliment_cool,compliment_cute,compliment_funny,compliment_hot,
                                        compliment_list, compliment_more, compliment_note, compliment_photos,compliment_plain,
                                        compliment_profile, compliment_writer, cool, fans,funny,name, review_count, useful,
                                        user_id, yelping_since)
                        VALUES ( %(average_stars)s, %(compliment_cool)s,%(compliment_cute)s,%(compliment_funny)s,%(compliment_hot)s,
                                %(compliment_list)s, %(compliment_more)s, %(compliment_note)s, %(compliment_photos)s,%(compliment_plain)s,
                                %(compliment_profile)s, %(compliment_writer)s, %(cool)s, %(fans)s,%(funny)s,%(name)s, %(review_count)s, %(useful)s,
                                %(user_id)s, %(yelping_since)s)
                """                      
                cursor.execute(sql, {
                    'average_stars': data[0],
                    'compliment_cool': data[1],
                    'compliment_cute': data[2],
                    'compliment_funny': data[3],
                    'compliment_hot': data[4],
                    'compliment_list': data[5],
                    'compliment_more': data[6],
                    'compliment_note': data[7],
                    'compliment_photos': data[8],
                    'compliment_plain': data[9],
                    'compliment_profile': data[10],
                    'compliment_writer': data[11],
                    'cool': data[12],
                    'fans': data[13],
                    'funny': data[14],
                    'name': data[15] ,
                    'review_count': data[16],
                    'useful': data[17],
                    'user_id': data[18],
                    'yelping_since': data[19]
                }) 
                conn.commit()
                data.clear()
                print("List has been inserted to business hours table successfully...")
        conn.close()
