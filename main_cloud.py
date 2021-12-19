from flask import Flask, render_template, request
# from hello_db import search_hello
# from light_db import search_light
# from daangn_db import search_daangn
import mysql.connector


def search_items(word):
    mydb = mysql.connector.connect(
        host="localhost",
        user="pracusername",
        password="test1234",
        database="test1"
    )

    mycursor = mydb.cursor()
    sql = f"SELCET * FROM products WHERE data like '%{word}5%'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    print(myresult)
    return


app = Flask("jgCloud")


@app.route("/")
def main():
    return render_template("1.html")


@app.route("/search")
def search():
    word = request.args.get('q')
    print(word)

    return render_template("search.html")


app.run(host="0.0.0.0")

search_items("피규어")
