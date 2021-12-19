import requests as req
from bs4 import BeautifulSoup as BS
import time
import json
import mysql.connector


def extract_page(word):
    turtle = str(time.time()).replace('.', '').strip()[0:13]
    hello_url = f"https://www.hellomarket.com/api/search/items?q={word}&page=1&startTime={turtle}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
    hello_res = req.get(hello_url, headers=headers)
    hello_soup = BS(hello_res.text, "html.parser")
    hello_json_txt = hello_soup.text
    hello_data = json.loads(hello_json_txt)

    total_count = hello_data["result"]["totalCount"]
    max_page = int(total_count)//30 + 1
    return max_page


def db_hello(word):
    turtle = str(time.time()).replace('.', '').strip()[0:13]
    cards = []

    mydb = mysql.connector.connect(
        host="localhost",
        user="pracusername",
        password="test1234",
        database="test1"
    )

    mycursor = mydb.cursor()

    for i in range(50):
        hello_url = f"https://www.hellomarket.com/api/search/items?q={word}&page={i+1}&startTime={turtle}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
        hello_res = req.get(hello_url, headers=headers)
        hello_soup = BS(hello_res.text, "html.parser")
        hello_json_txt = hello_soup.text
        hello_data = json.loads(hello_json_txt)

        for j in range(0, len(hello_data["list"])):
            if hello_data["list"][j].get("type") == "item":
                hello_product_image = hello_data["list"][j]["item"]["media"]["imageUrl"]
                hello_product_title = hello_data["list"][j]["item"]["title"]
                title_search = hello_product_title.replace(" ", "").lower()
                hello_product_price = hello_data["list"][j]["item"]["property"]["price"]["amount"]
                hello_product_loca_coord = hello_data["list"][j]["item"]["property"].get(
                    "location")
                try:
                    hello_product_loca = hello_product_loca_coord["address"]
                except:
                    hello_product_loca = None
                hello_product_id = hello_data["list"][j]["item"]["itemIdx"]
                hello_product_url = "https://www.hellomarket.com/item/" + \
                    str(hello_product_id) + \
                    "?viewPath=search_list&clickPath=search"
            else:
                continue

            card = {'url': hello_product_url, 'image': hello_product_image, 'title': hello_product_title, 'title_search': title_search, 'price': hello_product_price,
                    'location': hello_product_loca}
            cards.append(card)
            sql = "INSERT INTO products (market, url, image, title, title_search, price, location) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            val = ('hello', card['url'], card['image'], card['title'],
                   card['title_search'], card['price'], card['location'])
            mycursor.execute(sql, val)
            mydb.commit()
    mydb.close()
    return cards


db_hello("원피스")