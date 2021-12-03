from flask import Flask, render_template, request
from hello_scrap import hello
from light_scrap import light
from daangn_practice import search_daangn

app = Flask("jgCloud")


@app.route("/")
def main():
    return render_template("potato.html")


@app.route("/search")
def search():
    word = request.args.get('q')
    print(word)
    products = search_daangn(word) + hello(word) + light(word)

    return render_template("search.html", searchingBy=word, resultsNumber=len(products), word=word, products=products)


app.run(host="0.0.0.0")
