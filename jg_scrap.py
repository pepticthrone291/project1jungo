from bs4 import BeautifulSoup as BS
import requests as req
import json

data_1 = req.get("https://search-api.joongna.com/v25/search/product")
data_jg = req.post("https://search-api.joongna.com/v25/search/product", json={
    "filter": {"categoryDepth": 0, "categorySeq": 0,
               "dateFilterParameter": {"sortEndDate": None, "sortStartDate": None}, "flawedYn": 0,
               "fullPackageYn": 0, "limitedEditionYn": 0, "maxPrice": 2000000000, "minPrice": 0,
               "productCondition": -1, "tradeType": 0}, "osType": 2, "page": 4, "searchQuantity": 30,
    "searchStartTime": "2021-10-12 16:21:03", "searchWord": "아이패드", "sort": "RECOMMEND_SORT", "startIndex": 0,
    "productFilter": "APP"})
soup_jg = BS(data_jg.text, 'html.parser')
a = soup_jg.text
product_data = json.loads(a)
# print(product_data)

# for i in range(0, 10):
#     jg_product_image = product_data["data"]["items"][i]["detailImgUrl"]
#     jg_product_title = product_data["data"]["items"][i]["title"]
#     jg_product_price = product_data["data"]["items"][i]["price"]
#     jg_product_location = product_data["data"]["items"][i]["mainLocationName"]
#     jg_product_time = product_data["data"]["items"][i]["articleRegDate"]
# print(jg_product_image, jg_product_title, jg_product_price, jg_product_location, jg_product_time)

jg_product_image = product_data["data"]["items"][5]["detailImgUrl"]
print(jg_product_image)