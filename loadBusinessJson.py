import json
import db

def loadData():
    conn = db.dbConnection()
    cursor = conn.cursor()

    businessList = []

    print("Started Reading Business JSON file which contains multiple JSON document")
    #Creating a cursor object using the cursor() method    


    with open('yelp_business.json') as f:  
        for jsonObj in f:
            businessDict = json.loads(jsonObj)        
            businessList.append(businessDict['business_id'])
            businessList.append(businessDict['name'])
            businessList.append(businessDict['address'])
            businessList.append(businessDict['city'])
            businessList.append(businessDict['state'])        
            businessList.append(businessDict['postal_code'])
            businessList.append(businessDict['stars'])
            businessList.append(businessDict['review_count'])
                
            #print(jsonObj)
            print("Printing each JSON Decoded Object")
        
            print(businessList)
            sql = """
                INSERT INTO business (business_id, name, address, city,state, postal_code, stars,review_count, num_checkins, reviewrating)
                    VALUES (%(business_id)s, %(name)s, %(address)s, %(city)s, %(state)s, %(postal_code)s, %(stars)s, %(review_count)s, %(num_checkins)s, %(reviewrating)s );
            """
            print(sql)
            
        
            cursor.execute(sql, {
                'business_id': businessList[0], 
                'name': businessList[1], 
                'address': businessList[2],
                'city': businessList[3],
                'state': businessList[4], 
                'postal_code': businessList[5], 
                'stars': businessList[6], 
                'review_count': businessList[7],
                'num_checkins':0,
                'reviewrating':0.0
                }) 

    #     # Commit your changes in the database
            conn.commit()           
            businessList.clear()        
    conn.close()        
