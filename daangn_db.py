import requests
from bs4 import BeautifulSoup
from threading import Thread

daangn_result = 0


def extract(d, word, num):
    url_head = "https://www.daangn.com"
    res = requests.get(
        f"{url_head}/search/{word}/more/flea_market?page={str(num)}")
    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.select("article")

    page = []
    if len(articles) <= 1:
        global daangn_result
        daangn_result = 1
    for article in articles:
        url_tail = article.select_one("a")["href"]
        product_url = url_head + url_tail
        image = article.select_one("a > div.card-photo > img")['src']
        title = article.select_one(
            "a > div.article-info > div > span.article-title").text
        price = article.select_one(
            "a > div.article-info > p.article-price").text.strip()
        location = article.select_one(
            "a > div.article-info > p.article-region-name").text.strip()
        card = {'url': product_url, 'image': image,
                'title': title, 'price': price, 'location': location}
        page.append(card)
    d[num] = page
    return


def db_daangn(word):
    pages = {}
    threads = []
    for k in range(50):
        if daangn_result == 1:
            break
        t = Thread(target=extract, args=(pages, word, k+1))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    srtd = sorted(pages.items())
    posts = []
    for j in range(len(srtd)):
        element = srtd[j][1]
        posts = posts+element
    return posts
