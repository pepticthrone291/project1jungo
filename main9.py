import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, render_template, request


base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a stories by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


def extract_story(order_by):
    index = requests.get(order_by)
    soup = BeautifulSoup(index.text, "html.parser").text
    js = json.loads(soup)

    stories = []

    arts = js["hits"]
    for art in arts:
        if art:
            artid = art["objectID"]
            title = art["title"]
            link = art["url"]
            points = art["points"]
            author = art["author"]
            comments = art["num_comments"]
        else:
            continue
        story = {'id': artid, 'title': title, 'link': link,
                 'points': points, 'author': author, 'comments': comments}
        stories.append(story)
    return stories


def extract_comments(id):
    index = requests.get(make_detail_url(id))
    soup = BeautifulSoup(index.text, "html.parser").text
    if soup:
        js = json.loads(soup)

    boxes = []

    author_art = {'author_art': js["author"]}
    boxes.append(author_art)
    title = {'title': js["title"]}
    boxes.append(title)
    url = {'url': js["url"]}
    boxes.append(url)
    points = {'points': js["points"]}
    boxes.append(points)

    comments = js["children"]
    for comment in comments:
        if comment["author"]:
            author = comment["author"]+":"
            text = comment["text"]
        else:
            author = '[deleted]'
            text = None
        box = {'author': author, 'text': text}
        boxes.append(box)
    return boxes


db = {}
app = Flask("DayNine")


@app.route('/')
def home():
    order = request.args.get('order_by')
    if order == 'new':
        order_by = new
    else:
        order = 'popular'
        order_by = popular
    existing = db.get(order_by)
    if existing:
        stories = existing
    else:
        stories = extract_story(order_by)
        db[order_by] = stories
    return render_template('index9.html', order=order, stories=stories)


'''
@app.route('/')
def new():
  order_by = request.args.get('order_by')
  if order_by:
    existingStories = db.get(order_by)
    if existingStories:
      stories = existingStories
    else:
      stories = extract_story(order_by)
      db[order_by] = stories
  return render_template('index.html', stories = stories)
'''


@app.route('/<id>')
def artid(id):
    coms = extract_comments(id)
    return render_template('detail9.html', coms=coms)


app.run(host="0.0.0.0")
