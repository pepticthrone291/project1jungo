import requests as req
from bs4 import BeautifulSoup as BS
import json


hello_result = 0


def hello_scrap(word, num):
    hello_url = f"https://www.hellomarket.com/api/search/items?q={word}page=" + \
        str(num)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}
    hello_res = req.get(hello_url, headers=headers)
    hello_soup = BS(hello_res.text, "lxml")
    hello_json_txt = hello_soup.text
    hello_data = json.loads(hello_json_txt)

    cards = []

    if len(hello_data["list"]) <= 1:
        global hello_result
        hello_result = 1

    for i in range(0, len(hello_data["list"])):
        if hello_data["list"][i].get("type") == "item":
            hello_product_image = hello_data["list"][i]["item"]["media"]["imageUrl"]
            hello_product_title = hello_data["list"][i]["item"]["title"]
            hello_product_price = hello_data["list"][i]["item"]["property"]["price"]["amount"]
            hello_product_loca = hello_data["list"][i]["item"]["property"].get(
                "location")
            hello_product_time = hello_data["list"][i]["item"]["timeago"]
            hello_product_category = hello_data["list"][i]["item"]["categoryId"]
            hello_product_id = hello_data["list"][i]["item"]["itemIdx"]
            hello_product_url = "https://www.hellomarket.com/item/" + \
                str(hello_product_id) + "?viewPath=search_list&clickPath=search"

            # no location in hellomarket products mostly
            # time

        else:
            continue

        card = {'url': hello_product_url, 'title': hello_product_title, 'image': hello_product_image,  'price': hello_product_price,
                'location': hello_product_loca, 'time': hello_product_time, 'category': hello_product_category}
        cards.append(card)
    return cards


for i in range(5):
    print(hello_scrap("아이패드", i))
# t1 = time.perf_counter()

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
