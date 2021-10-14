import requests as req
from bs4 import BeautifulSoup as BS
from threading import Thread
import json
import time

hello_result = 0

def hello_scrap(num):
    hello_url = "https://www.hellomarket.com/api/search/items?q=%EC%95%84%EC%9D%B4%ED%8C%A8%EB%93%9C&page=" + str(num)
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}

    hello_res = req.get(hello_url, headers = headers)

    hello_soup = BS(hello_res.text, "lxml")
    
# hello_scrap(1)
    hello_json_txt = hello_soup.text
    hello_data = json.loads(hello_json_txt)
    if len(hello_data["list"]) <= 1:
        global hello_result
        hello_result = 1

    for i in range(0, len(hello_data["list"])):
        if hello_data["list"][i].get("type") == "item":
            hello_product_image = hello_data["list"][i]["item"]["media"]["imageUrl"]
            hello_product_title = hello_data["list"][i]["item"]["title"]
            hello_product_price = hello_data["list"][i]["item"]["property"]["price"]["text"]
            hello_product_loca = hello_data["list"][i]["item"]["property"].get("location")
            hello_product_category = hello_data["list"][i]["item"]["categoryId"]
            hello_product_id = hello_data["list"][i]["item"]["itemIdx"]
            hello_product_url = "https://www.hellomarket.com/item/" + str(hello_product_id) + "?viewPath=search_list&clickPath=search"

            # no location in hellomarket products mostly
            # time

        else:
            continue
        
        print(hello_product_image, hello_product_title, hello_product_price, hello_product_loca, hello_product_category, hello_product_url)

t1 = time.perf_counter()

hello_scrap(1)
# hello_scrap(2)
# hello_scrap(3)
# hello_scrap(4)
# hello_scrap(5)

t2 = time.perf_counter()

print(f'Finished in {round(t2-t1, 2)} second(s)')

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
