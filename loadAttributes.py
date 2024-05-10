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
            attrs = businessDict['attributes']
            businessList.append(businessDict['business_id'])
            businessList.append(businessDict['latitude'])
            businessList.append(businessDict['longitude'])
            businessList.append(businessDict['is_open'])
                                   
            # if attrs['BusinessAcceptsCreditCards'] not in attrs:
            #     attrs['BusinessAcceptsCreditCards'] = False                
            # businessList.append(attrs['BusinessAcceptsCreditCards'])
            
            # if attrs['RestaurantsPriceRange2'] not in attrs:
            #     attrs['RestaurantsPriceRange2'] = 0
            # businessList.append(attrs['RestaurantsPriceRange2'])    
            
            # if attrs['BikeParking'] not in attrs:
            #     attrs['BikeParking'] = False
            # businessList.append(attrs['BikeParking'])
            
            # if attrs['GoodForKids'] not in attrs:
            #     attrs['GoodForKids'] = False
            # businessList.append(attrs['GoodForKids'])    
            if 'BusinessParking' in attrs:
               
                opts = attrs['BusinessParking']               
                if(len(opts) > 0):
                    businessList.append(opts['garage'])
                    businessList.append(opts['street'])
                    businessList.append(opts['validated'])
                    businessList.append(opts['lot'])
                    businessList.append(opts['valet'])
           
            print("Printing each JSON Decoded Object")
        
            print(businessList)
            sql = """
                INSERT INTO attributes ( business_id,latitude,longitude, is_open)
                    VALUES (%(business_id)s,%(latitude)s,%(longitude)s, %(is_open)s);
            """
            
            cursor.execute(sql, {
                'business_id':businessList[0],
                'latitude': businessList[1],
                'longitude': businessList[2],
                'is_open': businessList[3]                                            
                
                })


    #     # Commit your changes in the database
            conn.commit()           
            businessList.clear()        
    conn.close()        
