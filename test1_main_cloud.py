from flask import Flask, render_template, request
from search_test_1_practice import search_items

app = Flask("jgCloud")


@app.route("/")
def main():
    return render_template("1.html")


@app.route("/search")
def search():
    word = request.args.get('q')
    print(word)
    items = search_items(word)

    return render_template("search.html", searchingBy=word, word=word, items=items)


app.run(host="0.0.0.0")
