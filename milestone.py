import sys
from PyQt5.QtWidgets import (QPushButton,QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout)
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap

import psycopg2
import db
qtCreatorFile = "milestone1.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    
    def __init__(self):
        super(milestone1, self).__init__()
        
        # to control the change state of each component (city, zip, category and business) when it is cleared/changed
        self.cityIgnore = False
        self.zipIgore = False
        self.catIgnore = False
        self.businessIgnore = False
        self.loadPopularBusinessIgnore = False
        self.loadSuccessfulBusinessIgnore = False
        self.loadDataIgnore = False
        
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Page 1
        # loadStateList query the distinct state from the business table 
        # and create the list object and bind it to the statelist element in the ui
        self.loadStateList()        
        #self.loadPopularBusinessByZipcode()
       # on state change event stateChanged method is called to clear the existing city list 
       # and regenerate the city list with new state selection 
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
       
       # On city change event cityChanged method is called to clear the zip code 
       # and regenerate the zipcode list with new city and state selection 
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        
        # on zipcode change event zipcodeChanged is called to clear the existing category of business
        # And regenerate the new category list by zip code, city, and state selection by user
        self.ui.zipcode.itemSelectionChanged.connect(self.zipcodeChanged)
        
        # On category select render/display the business on the right side table widget       
        self.ui.categoryList.itemSelectionChanged.connect(self.loadBuinessByCategory)
        
        # refresh button reload the data by selected zipcode
        self.ui.loadDataByZipcode.clicked.connect(self.loadData)
        
        # on lookup buttin click generate the business table
        self.ui.lookup.clicked.connect(self.loadLookup)
        
        # clear the business table clicking delete/clear button
        self.ui.clearSearch.clicked.connect(self.clearSerach)
           
    
    def clearSerach(self):
        self.ui.businessTable.clear()
    # Connecting to db and executing the queries     
    def executeQuery(self,sql_str):
        try:
            conn = db.dbConnection() #psycopg2.connect("dbname='milestone1db' user= 'postgres' host='localhost' password='password' port='5432' ")   
        except:
            print('Unable to connect to the database')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result 

    # get the state list from Database to load
    def getStateList(self):
        sql_str = "SELECT distinct state FROM business ORDER BY state;"                
        try:
            results = self.executeQuery(sql_str)
            return results
        except:            
            print('Query Failed')
    
    # creating the state list        
    def loadStateList(self):
        self.ui.stateList.clear()     
        try:
            results = self.getStateList()
            self.ui.stateList.addItem("Select State")
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:            
            self.ui.stateList.setCurrentIndex(-1)
            self.ui.stateList.setCurrentIndex(0)
            self.ui.stateList.clearEditText()
    
    # on state change, clearing the data from other controls and populating after the selection                    
    def stateChanged(self):
        self.cityIgnore = True
        self.zipIgore = True
        self.catIgnore = True
        
        self.ui.cityList.clear()
        self.ui.zipcode.clear()
        
        #Zip code Stat
        self.ui.numOfBusinesses.clear()
        self.ui.totalPopulation.clear()
        self.ui.avgIncome.clear()
        self.ui.topCategoryTable.clear()
        
        #category and business
        self.ui.categoryList.clear()
        
        self.cityIgnore = False
        self.zipIgore = False
        self.catIgnore = False      
        state = self.ui.stateList.currentText()       
        
             
        if (self.ui.stateList.currentIndex() >= 0):
            
            sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"    
            try:
                results = self.executeQuery(sql_str)                                
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query Failed")         

    # on city change clear the data from dependent controllers like zip code and categories 
    def cityChanged(self):
        
        if self.cityIgnore:
            self.cityIgnore =False
            return
        #on change of state or city clear the zip code
        self.zipIgore = True
        self.ui.zipcode.clear()
        
        #Zip code stat
        self.ui.numOfBusinesses.clear()
        self.ui.totalPopulation.clear()
        self.ui.avgIncome.clear()
        self.ui.topCategoryTable.clear()
        
        # clear category and business list when city change
        self.catIgnore = True
        self.ui.categoryList.clear()         
        
        self.zipIgore = False
        self.catIgnore = False
        
                 
        if(self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()            
            for c in self.ui.cityList.selectedItems():               
                city = self.ui.cityList.selectedItems()[0].text()
                sql_str = "SELECT distinct postal_code FROM business WHERE city = '" + city + "' and state = '" +state+ "';" 
                try:
                    results = self.executeQuery(sql_str)
                    for row in results:
                        self.ui.zipcode.addItem(row[0])                    
                except:
                    print("Query Failed")

    # on zip code change clearing the category ad business table re populating with next selection
    def zipcodeChanged(self):
       
        if self.zipIgore:
            self.zipIgore =False
            return 
        self.catIgnore = True
        self.ui.categoryList.clear()        
        self.catIgnore = False        
             
        if(self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipcode.selectedItems()) > 0):
            state = self.ui.stateList.currentText()            
            for c in self.ui.cityList.selectedItems():               
                city = self.ui.cityList.selectedItems()[0].text()
            for z in self.ui.zipcode.selectedItems():
                zip = self.ui.zipcode.selectedItems()[0].text()   
        self.getNumberOfBusinesses(zip)
        self.getPopulationAndIncome(zip)
        self.getCategories(state,city,zip)
        self.getTopCategoryTable(zip)             
    
    # creating the category list
    def getCategories(self, state,city,zip):
        sql_str = "SELECT distinct category_name FROM category c join business b on c.business_id = b.business_id WHERE postal_code = '"+ zip +"' ORDER BY category_name;" 
        try:
            results = self.executeQuery(sql_str)
            for row in results:               
                self.ui.categoryList.addItem(row[0])
        except Exception as e:
            print("Query Failed", e)
            
    # action method - lookup business by state, city and zipcode selection 
    def loadLookup(self):
        print(self.ui.stateList.currentIndex() == 0)
        print()
        if(len(self.ui.zipcode.selectedItems()) == 0):
            return
        if self.zipIgore:
            self.zipIgore =False
            return 
        self.loadDataIgnore = False
        self.getBusiness()         
    
    # get business by category 
    def loadBuinessByCategory(self):
        if(len(self.ui.categoryList.selectedItems()) > 0):
            for ct in self.ui.categoryList.selectedItems():
                category = self.ui.categoryList.selectedItems()[0].text()
            self.getBusiness(category) 
                
    # createing the business table    
    def getBusiness(self, category=''):
        
        if(self.ui.stateList.currentIndex() == 0) and (len(self.ui.cityList.selectedItems()) == 0) and (len(self.ui.zipcode.selectedItems()) == 0):  
            return         
        state = self.ui.stateList.currentText()            
        for c in self.ui.cityList.selectedItems():               
            city = self.ui.cityList.selectedItems()[0].text()
        for z in self.ui.zipcode.selectedItems():
            zip = self.ui.zipcode.selectedItems()[0].text()
        sql_str = "SELECT distinct name, address, city, stars,review_count, reviewrating, num_checkins FROM business b join category c on b.business_id = c.business_id WHERE state = '" + state + "' AND city = '" + city + "' and postal_code ='"+zip+"' "   
        if(len(category)> 0):
            sql_str += "and category_name like '%"+category+"%'"
        sql_str += " ORDER BY name;"  
        print(sql_str)     
        try:            
            results = self.executeQuery(sql_str)       
            self.ui.businessTable.setColumnCount(len(results[0])) 
            self.ui.businessTable.setRowCount(len(results)) 
            self.ui.businessTable.horizontalHeader().setFixedHeight(60)
            self.ui.businessTable.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address','City','Stars','Review Count','Review Rating','Number of Checkins'] )           
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0,240)
            self.ui.businessTable.setColumnWidth(1,210)
            self.ui.businessTable.setColumnWidth(2,100)
            self.ui.businessTable.setColumnWidth(3,100)
            self.ui.businessTable.setColumnWidth(4,100)
            self.ui.businessTable.setColumnWidth(5,100)
            self.ui.businessTable.setColumnWidth(6,100)
            currentRowCount = 0
        
            for row in results:                
                for colCount in range (0,(len(results[0]))):                  
                    self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
            
        except:
            print("Query Failed") 
            
    # creating the Zip code stats on the right side of ui        
    def getNumberOfBusinesses(self,zip):        
        sql_str = "SELECT count(*) as num FROM business WHERE postal_code = '" + zip +"';"     
        
        try:
            results = self.executeQuery(sql_str)
            self.ui.numOfBusinesses.setText(str(results[0][0]))
        except: 
            print("Query Failed")
    
    # zip code stats
    def getPopulationAndIncome(self,zip):        
        sql_str = "SELECT population, "'"meanIncome"'" FROM "'"zipcodeData"'" WHERE zipcode = '" + zip +"';" 
        try:
            results = self.executeQuery(sql_str)        
            self.ui.totalPopulation.setText(str(results[0][0]))
            self.ui.avgIncome.setText(str(results[0][1]))
        except: 
            print("Query Failed")
    
    # top categories by zip code               
    def getTopCategoryTable(self,zip):
        sql_str = "with dd as (select distinct name, max(b.business_id) as buss_id from business b join category ct on b.business_id = ct.business_id where postal_code = '"+zip+"' group by name) select count(business_id), category_name from dd join category ct on dd.buss_id = ct.business_id group by category_name order by 1 desc"  
        
        try:
            results = self.executeQuery(sql_str)
           
            self.ui.topCategoryTable.setColumnCount(len(results[0])) 
            self.ui.topCategoryTable.setRowCount(len(results)) 
           
            self.ui.topCategoryTable.horizontalHeader().setFixedHeight(50)
            self.ui.topCategoryTable.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
            self.ui.topCategoryTable.setHorizontalHeaderLabels(['# Of Business','Category'] )           
            self.ui.topCategoryTable.resizeColumnsToContents()
            self.ui.topCategoryTable.setColumnWidth(0,90)
            self.ui.topCategoryTable.setColumnWidth(1,150)
            currentRowCount = 0
         
            for row in results:                
                for colCount in range (0,(len(results[0]))):                  
                    self.ui.topCategoryTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
        except Exception as e: 
            print("Query Failed", e)
            
    # action method - on click the refresh push button generates the popular and successful business table in the bottom
    def loadData(self):       
        if(len(self.ui.zipcode.selectedItems()) == 0): 
            return
        if self.zipIgore:
            self.zipIgore =False
            return 
        self.loadDataIgnore = False       
        
                   
        for z in self.ui.zipcode.selectedItems():
            zip = self.ui.zipcode.selectedItems()[0].text()
        self.loadPopularBusinessByZipcode(zip)
        self.loadSuccessfulBusiness(zip)        
            
    # creatng the popular business        
    def loadPopularBusinessByZipcode(self, zip):
        sql_str = sql_str = "SELECT distinct name,stars, reviewrating, review_count FROM business WHERE postal_code ='"+zip+"' order by reviewrating desc;"
        try:
            results = self.executeQuery(sql_str)
           
            self.ui.popularBusinessTable.setColumnCount(len(results[0])) 
            self.ui.popularBusinessTable.setRowCount(len(results)) 
           
            self.ui.popularBusinessTable.horizontalHeader().setFixedHeight(60)
            self.ui.popularBusinessTable.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
            self.ui.popularBusinessTable.setHorizontalHeaderLabels(['Business Name','Stars','Review Rating','# of Reviews'] )           
            self.ui.popularBusinessTable.resizeColumnsToContents()
            self.ui.popularBusinessTable.setColumnWidth(0,210)
            self.ui.popularBusinessTable.setColumnWidth(1,70)
            self.ui.popularBusinessTable.setColumnWidth(2,90)
            self.ui.popularBusinessTable.setColumnWidth(3,70)
            currentRowCount = 0
         
            for row in results:                
                for colCount in range (0,(len(results[0]))):                  
                    self.ui.popularBusinessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1                
        except Exception as e: 
            print("Query Failed", e)
    
    #creating the successful business by zipcode - business have more checkin than other businesses and have been market for longer time and despite the less review count or rating some business still have customer coming to the place    
    def loadSuccessfulBusiness(self, zip):
        sql_str = sql_str = "with rating as (select business_id, min(date) as dd from review r group by business_id) select name, reviewrating, num_checkins,review_count from rating ci join business b on ci.business_id = b.business_id where postal_code ='"+zip+"'order by num_checkins desc , review_count desc;" 
        
        try:
            results = self.executeQuery(sql_str)
           
            self.ui.successfulBusinessTable.setColumnCount(len(results[0])) 
            self.ui.successfulBusinessTable.setRowCount(len(results)) 
           
            self.ui.successfulBusinessTable.horizontalHeader().setFixedHeight(60)
            self.ui.successfulBusinessTable.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
            self.ui.successfulBusinessTable.setHorizontalHeaderLabels(['Business Name', 'Review Rating','# of Checkins','# of Reviews'] )           
            self.ui.successfulBusinessTable.resizeColumnsToContents()
            self.ui.successfulBusinessTable.setColumnWidth(0,210)
            self.ui.successfulBusinessTable.setColumnWidth(1,90)
            self.ui.successfulBusinessTable.setColumnWidth(2,90)
            self.ui.successfulBusinessTable.setColumnWidth(3,70)
            currentRowCount = 0
         
            for row in results:                
                for colCount in range (0,(len(results[0]))):                  
                    self.ui.successfulBusinessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1                
        except Exception as e: 
            print("Query Failed", e)
                             
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())

