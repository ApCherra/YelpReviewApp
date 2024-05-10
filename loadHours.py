import json

import db
def loadData():
    conn = db.dbConnection()
    print("Started Reading Business JSON file which contains multiple JSON document")
    #Creating a cursor object using the cursor() method    
    cursor = conn.cursor()
    hoursList = []
    with open('yelp_business.json') as f:  
        for jsonObj in f:
            businessDict = json.loads(jsonObj)           
            hoursData = businessDict['hours']
                     
            if(len(hoursData) > 0):
                for hl in hoursData:                   
                    hoursList.append(businessDict['business_id'])
                    hoursList.append(hl)
                    hoursList.append(hoursData.get(hl))
                    
                    sql = """
                        INSERT INTO business_hours (business_id,day, hours)
                            VALUES (  %(business_id)s, %(day)s, %(hours)s);
                    """
                    print(hoursList[0])
                    print(hoursList[1])
                    print(hoursList[2])
                    cursor.execute(sql, {
                        'business_id': hoursList[0],
                        'day': hoursList[1],
                        'hours': hoursList[2]
                    }) 
                    conn.commit()
                    hoursList.clear()
                    print("List has been inserted to business hours table successfully...")
        conn.close()

