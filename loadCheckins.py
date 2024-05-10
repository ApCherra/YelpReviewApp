import json

import db
def loadData():
    conn = db.dbConnection()
    print("Started Reading Checkins JSON file which contains multiple JSON document")
    #Creating a cursor object using the cursor() method    
    cursor = conn.cursor()
    checkinsList = []
    with open('yelp_checkin.json') as f:  
        for jsonObj in f:
            dict = json.loads(jsonObj)           
            checkinTimes = dict['time']           
         
            if(len(dict) > 0):
                for ci in checkinTimes:
                    checkins = checkinTimes.get(ci)
                    print(checkins)
                    for i in checkins:
                        checkinsList.append(dict['business_id'])
                        checkinsList.append(ci)
                        checkinsList.append(i)                        
                        checkinsList.append(checkins.get(i))
                    
                        sql = """
                            INSERT INTO checkins (business_id, day, time, num_of_checkins)
                                VALUES (  %(business_id)s, %(day)s, %(time)s, %(num_of_checkins)s);
                        """
                        print(checkinsList[0])
                        print(checkinsList[1])
                        print(checkinsList[2])
                        print(checkinsList[3])
                        cursor.execute(sql, {
                            'business_id': checkinsList[0],
                            'day': checkinsList[1],
                            'time': checkinsList[2],
                            'num_of_checkins': checkinsList[3]
                        }) 
                        conn.commit()
                        checkinsList.clear()
                        print("List has been inserted to business hours table successfully...")
        conn.close()

