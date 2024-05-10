import json
import db
import loadBusinessJson
import loadCatagory
import loadHours
import loadCheckins
import loadReview
import loadUser
import loadFriends
import loadAttributes

print("Started Reading JSON file which contains multiple JSON document")
#Creating a cursor object using the cursor() method

   
print("Started Reading Business JSON file which contains multiple JSON document")    
#loadBusinessJson.loadData()
#loadCatagory.loadData()
#loadHours.loadData()
#loadCheckins.loadData()
#loadReview.loadData()
#loadUser.loadData()
#loadFriends.loadData()
loadAttributes.loadData()
print ('data load is completed')
# #close connection
