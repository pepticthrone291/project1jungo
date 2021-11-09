import requests as req
from bs4 import BeautifulSoup as BS
# import concurrent.futures
# from threading import Thread
import json
import datetime
import time

light_result = 0


def light_scrap(word, num):
    light_url = f"https://api.bunjang.co.kr/api/1/find_v2.json?q={word}&order=score&page={str(num)}&request_id=20211011122439&stat_device=w&n=100&stat_category_required=1&req_ref=search&version=4"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}

    light_res = req.get(light_url, headers=headers)

    light_soup = BS(light_res.text, "html.parser")
    light_json_text = light_soup.text
    light_data = json.loads(light_json_text)

    cards = []

    if len(light_data["list"]) <= 1:
        global light_result
        light_result = 1

    for j in range(0, len(light_data["list"])-1):
        if light_data["list"][j].get("ad") == False:
            light_product_image = light_data["list"][j]["product_image"]
            light_product_title = light_data["list"][j]["name"]
            light_product_price = light_data["list"][j]["price"]
            light_product_loca = light_data["list"][j]["location"]
            light_product_time_a = light_data["list"][j]["update_time"]
            light_product_time = datetime.timedelta(
                seconds=time.time() - float(light_product_time_a))
            # category needed
            light_product_id = light_data["list"][j]["pid"]
            light_product_detail_url = "https://api.bunjang.co.kr/api/1/product/" + \
                light_product_id + "/detail_info.json?version=4"
            light_detail_res = req.get(
                light_product_detail_url, headers=headers)

            light_detail_soup = BS(light_detail_res.text, "html.parser")
            light_detail_json_text = light_detail_soup.text
            light_detail_data = json.loads(light_detail_json_text)

            light_product_category = light_detail_data["item_info"]["category_id"]

            light_product_url = f"https://m.bunjang.co.kr/products/{light_product_id}?q=%ED%99%94%EC%9D%B4%ED%8A%B8%EB%B3%B4%EB%93%9C&ref=%EA%B2%80%EC%83%89%EA%B2%B0%EA%B3%BC"
        else:
            continue

        card = {'url': light_product_url, 'title': light_product_title, 'image': light_product_image,  'price': light_product_price,
                'location': light_product_loca, 'time': light_product_time, 'category': light_product_category}
        cards.append(card)
    return cards


# t1 = time.perf_counter()

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     pages = [0, 1, 2, 3, 4]
#     # results = [executor.submit(light_scrap, page) for page in pages]
#     # for f in concurrent.futures.as_completed(results):
#     #     print(f.result())
#     results = executor.map(light_scrap, pages)

# t2 = time.perf_counter()

# print(f'Finished in {round(t2-t1, 2)} second(s)')


# t1 = time.perf_counter()

# threads = []
# k = 0

# while 1:
#     if light_result == 1:
#         break
#     t = Thread(target=light_scrap, args=[k])
#     t.start()
#     threads.append(t)
#     k += 1

# for thread in threads:
#     thread.join()

# t2 = time.perf_counter()
# print(t2 - t1)
