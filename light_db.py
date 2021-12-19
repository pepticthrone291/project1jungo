import requests as req
from bs4 import BeautifulSoup as BS
import json
from threading import Thread

light_result = 0


def light_page(d, word, num):
    page = []
    light_url = f"https://api.bunjang.co.kr/api/1/find_v2.json?q={word}&order=score&page={str(num)}&request_id=20211011122439&stat_device=w&n=100&stat_category_required=1&req_ref=search&version=4"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}

    light_res = req.get(light_url, headers=headers)
    light_soup = BS(light_res.text, "html.parser")
    light_json_text = light_soup.text
    light_data = json.loads(light_json_text)

    if len(light_data["list"]) <= 1:
        global light_result
        light_result = 1

    for j in range(0, len(light_data["list"])-1):
        if light_data["list"][j].get("ad") == False:
            light_product_image = light_data["list"][j]["product_image"]
            light_product_title = light_data["list"][j]["name"]
            light_product_price = light_data["list"][j]["price"]
            light_product_loca = light_data["list"][j]["location"]
            light_product_id = light_data["list"][j]["pid"]
            light_product_url = f"https://m.bunjang.co.kr/products/{light_product_id}?q=%ED%99%94%EC%9D%B4%ED%8A%B8%EB%B3%B4%EB%93%9C&ref=%EA%B2%80%EC%83%89%EA%B2%B0%EA%B3%BC"
        else:
            continue

        card = {'url': light_product_url, 'image': light_product_image,  'title': light_product_title, 'price': light_product_price,
                'location': light_product_loca}
        page.append(card)
    d[num] = page
    return


def db_light(word):
    j = 0
    lala = {}
    threads = []
    while True:
        if light_result == 1:
            break
        t = Thread(target=light_page, args=(lala, word, j))
        t.start()
        threads.append(t)
        j += 1
    for thread in threads:
        thread.join()
    items = []
    sorting_items = sorted(lala.items())
    for k in range(len(sorting_items)):
        element = sorting_items[k][1]
        items = items + element
    return items