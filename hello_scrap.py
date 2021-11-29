import requests as req
from bs4 import BeautifulSoup as BS
import time
import json


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


def hello(word):
    turtle = str(time.time()).replace('.', '').strip()[0:13]
    cards = []
    for i in range(extract_page(word)):
        hello_url = f"https://www.hellomarket.com/api/search/items?q={word}&page={i+1}&startTime={turtle}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
        hello_res = req.get(hello_url, headers=headers)
        hello_soup = BS(hello_res.text, "lxml")
        hello_json_txt = hello_soup.text
        hello_data = json.loads(hello_json_txt)

        for j in range(0, len(hello_data["list"])):
            if hello_data["list"][j].get("type") == "item":
                hello_product_image = hello_data["list"][j]["item"]["media"]["imageUrl"]
                hello_product_title = hello_data["list"][j]["item"]["title"]
                hello_product_price = hello_data["list"][j]["item"]["property"]["price"]["amount"]
                hello_product_loca = hello_data["list"][j]["item"]["property"].get(
                    "location")
                hello_product_time = hello_data["list"][j]["item"]["timeago"]
                hello_product_category = hello_data["list"][j]["item"]["categoryId"]
                hello_product_id = hello_data["list"][j]["item"]["itemIdx"]
                hello_product_url = "https://www.hellomarket.com/item/" + \
                    str(hello_product_id) + \
                    "?viewPath=search_list&clickPath=search"
            else:
                continue

            card = {'url': hello_product_url, 'title': hello_product_title, 'image': hello_product_image,  'price': hello_product_price,
                    'location': hello_product_loca, 'time': hello_product_time, 'category': hello_product_category}
            cards.append(card)
    return cards

# threads = []
# j = 0

# while 1:
#     j += 1
#     if hello_result == 1:
#         break
#     t = Thread(target=hello_scrap, args=[j])
#     t.start()
#     threads.append(t)

# for thread in threads:
#     thread.join()

# t2 = time.perf_counter()
# print(t2 - t1)
# print(len(data_hello["list"]))

# product_title_hello = data_hello["list"][0]["item"]["title"]
# print(product_title_hello)


#     if len(data_hello) <= 1:
#         global result
#         result = 0
#     else:
#         for i in len(data_hello):
#             product_image_hello = data_hello["list"][i]["item"]["media"]["imageUrl"]
#             product_title_hello = data_hello["list"][i]["title"]
#             product_price_hello = data_hello["list"][i]["property"]["price"]["text"]
#             print(product_image_hello, product_title_hello, product_price_hello)
print(hello("화이트보드"))
