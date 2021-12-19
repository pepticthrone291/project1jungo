import requests
from bs4 import BeautifulSoup
# from threading import Thread
import mysql.connector

daangn_result = 0


def extract(d, word, num):
    url_head = "https://www.daangn.com"

    mydb = mysql.connector.connect(
        host="localhost",
        user="pracusername",
        password="test1234",
        database="test1"
    )

    mycursor = mydb.cursor()

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
        title_search = title.replace(" ", "").lower()
        price_unit = article.select_one(
            "a > div.article-info > p.article-price").text.strip()
        try:
            price = int(price_unit.replace(",", "").replace("원", ""))
        except:
            price = None
        location = article.select_one(
            "a > div.article-info > p.article-region-name").text.strip()
        card = {'url': product_url, 'image': image,
                'title': title, 'title_search': title_search, 'price': price, 'location': location}
        page.append(card)

        sql = "INSERT INTO products (market, url, image, title, title_search, price, location) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        val = ('daangn', card['url'], card['image'], card['title'],
               card['title_search'], card['price'], card['location'])
        mycursor.execute(sql, val)
        mydb.commit()
    mydb.close()
    d[num] = page
    return


def db_daangn(word):
    pages = {}
    # threads = []
    for k in range(50):
        # if daangn_result == 1:
        #     break
        #     t = Thread(target=extract, args=(pages, word, k+1))
        #     t.start()
        #     threads.append(t)
        # for thread in threads:
        #     thread.join()
        extract(pages, word, k+1)
    srtd = sorted(pages.items())
    posts = []
    for j in range(len(srtd)):
        element = srtd[j][1]
        posts = posts+element
    return posts


db_daangn("원피스")
