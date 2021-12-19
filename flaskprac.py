from flask import Flask, render_template, request, redirect
from carrot_scrap import carrot_scrap
from hello_search import hello_scrap
from light_db import light_scrap

app = Flask("JGscrp")

db = {}


@app.route("/")
def home():
    return render_template("potato.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingItems = db.get(word)
        if existingItems:
            items = existingItems
        else:
            items = light_scrap(word, 1)
            db[word] = items
    else:
        return redirect("/")
    return render_template("report.html", searchingBy=word, resultsNumber=len(items), items=items)


app.run(host="0.0.0.0")
