import requests
from bs4 import BeautifulSoup
import json


base_url = "http://hn.algolia.com/api/v1"

popular = f"{base_url}/search?tags=story"


def make_detail_url(id):
    return f"{base_url}/items/{id}"


index = requests.get(make_detail_url(id))
soup = BeautifulSoup(index.text, "html.parser").text
js = json.loads(soup)

boxes = []

comments = js["children"]
for comment in comments:
    author = comment["author"]
    if author is None:
        author = "[deleted]"
    text = comment["text"]
    box = {'author': author, 'text': text}
    boxes.append(box)

print(boxes)
