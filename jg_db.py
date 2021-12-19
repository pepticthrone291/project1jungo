from bs4 import BeautifulSoup as BS
import requests as req
import json
import time


def db_jg(word):
    cards = []
    url_head = "https://m.joongna.com/product-detail/"
    for num in range(3):
        current_time = time.strftime('%Y-%m-%d %X')
        data_jg = req.post("https://search-api.joongna.com/v25/search/product", json={
            "filter": {"categoryDepth": 0, "categorySeq": 0,
                       "dateFilterParameter": {"sortEndDate": None, "sortStartDate": None}, "flawedYn": 0,
                       "fullPackageYn": 0, "limitedEditionYn": 0, "maxPrice": 2000000000, "minPrice": 0,
                       "productCondition": -1, "tradeType": 0}, "osType": 2, "page": 1, "searchQuantity": num + 1,
            "searchStartTime": current_time, "searchWord": f"{word}", "sort": "RECOMMEND_SORT", "startIndex": 0,
            "productFilter": "APP"})
        soup_jg = BS(data_jg.text, 'html.parser')
        a = soup_jg.text
        product_data = json.loads(a)
        # print(product_data)

        # for i in range(0, 10):
        #     jg_product_image = product_data["data"]["items"][i]["detailImgUrl"]
        #     jg_product_title = product_data["data"]["items"][i]["title"]
        #     jg_product_price = product_data["data"]["items"][num]["price"]
        #     jg_product_location = product_data["data"]["items"][num]["mainLocationName"]
        #     jg_product_time = product_data["data"]["items"][num]["articleRegDate"]
        # print(jg_product_image, jg_product_title, jg_product_price, jg_product_location, jg_product_time)
        if len(product_data["data"]["items"]) + 1 == num + 1:
            break
        jg_product_id = str(product_data["data"]["items"][num]["seq"])
        jg_product_url = url_head + jg_product_id
        jg_product_image = product_data["data"]["items"][num]["detailImgUrl"]
        jg_product_title = product_data["data"]["items"][num]["title"]
        jg_product_price = product_data["data"]["items"][num]["price"]
        jg_product_location = product_data["data"]["items"][num]["mainLocationName"]
        card = {'url': jg_product_url, 'image': jg_product_image, 'title': jg_product_title,
                'price': jg_product_price, 'location': jg_product_location}
        cards.append(card)
    return cards


print(db_jg("원피스"))
