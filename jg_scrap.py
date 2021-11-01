from bs4 import BeautifulSoup as BS
import requests as req
import json

# data_1 = req.get("https://search-api.joongna.com/v25/search/product")
data_jg = req.post("https://search-api.joongna.com/v25/search/product", json={
    "filter": {"categoryDepth": 0, "categorySeq": 0,
               "dateFilterParameter": {"sortEndDate": None, "sortStartDate": None}, "flawedYn": 0,
               "fullPackageYn": 0, "limitedEditionYn": 0, "maxPrice": 2000000000, "minPrice": 0,
               "productCondition": -1, "tradeType": 0}, "osType": 2, "page": 1, "searchQuantity": 3,
    "searchStartTime": "2021-11-01 16:21:03", "searchWord": "아이패드", "sort": "RECOMMEND_SORT", "startIndex": 0,
    "productFilter": "APP"})
soup_jg = BS(data_jg.text, 'html.parser')
a = soup_jg.text
product_data = json.loads(a)

# json 데이터를 텍스트 형식으로 볼 수 있음
# print(product_data)

# 상품 이미지, 제목, 가격, 위치, 시간 반복 크롤링
# for i in range(0, 10):
#     jg_product_image = product_data["data"]["items"][i]["detailImgUrl"]
#     jg_product_title = product_data["data"]["items"][i]["title"]
#     jg_product_price = product_data["data"]["items"][i]["price"]
#     jg_product_location = product_data["data"]["items"][i]["mainLocationName"]
#     jg_product_time = product_data["data"]["items"][i]["articleRegDate"]
# print(jg_product_image, jg_product_title, jg_product_price, jg_product_location, jg_product_time)

# jg_product_image = product_data["data"]["items"][1]["detailImgUrl"]
# print(jg_product_image)