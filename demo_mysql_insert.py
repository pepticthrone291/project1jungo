import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="pracusername",
    password="test1234",
    database="opentutorials"
)

mycursor = mydb.cursor()

sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("YANG", "Highway 21")

mycursor.execute(sql, val)

mydb.commit()


