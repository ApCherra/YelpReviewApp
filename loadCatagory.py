import json

import db
def loadData():
    categoryList = []
    conn = db.dbConnection()
    print("Started Reading Business JSON file which contains multiple JSON document")
    #Creating a cursor object using the cursor() method    
    cursor = conn.cursor()
    with open('yelp_business.json') as f:  
        for jsonObj in f:
            businessDict = json.loads(jsonObj) 
            categoryList = []
            categoryData = businessDict['categories']
            
            for dd in categoryData:
                print(dd)
                categoryList.append(businessDict['business_id'])
                categoryList.append(dd)
                
                sql = """
                    INSERT INTO category (business_id,category_name)
                        VALUES (  %(business_id)s, %(category_name)s);
                """
                print(sql)
                print(categoryList[0])
                print(categoryList[1])
                cursor.execute(sql, {            
                   
                    'business_id': categoryList[0],
                    'category_name': categoryList[1]
                }) 
                conn.commit()
                categoryList.clear()
                print("List has been inserted to category table successfully...")
        conn.close()

