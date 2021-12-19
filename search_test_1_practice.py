import mysql.connector


def search_items(word):
    mydb = mysql.connector.connect(
        host="localhost",
        user="pracusername",
        password="test1234",
        database="test1"
    )

    mycursor = mydb.cursor()
    sql = f"SELECT * FROM products WHERE title_search like \'%{word}%\'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult
