import psycopg2

def dbConnection():
    conn = psycopg2.connect(
        database="milestone1db", user='postgres', password='password', host='127.0.0.1', port= '5432'
    )
    #Creating a cursor object using the cursor() method
    
    return conn