from bs4 import BeautifulSoup as BS
import requests as req
from threading import Thread
import time

result = 0

def carrot_scrap(num):
    carrot_main_url = "https://www.daangn.com"
    carrot_url = carrot_main_url + "/search/%ED%99%94%EC%9D%B4%ED%8A%B8%EB%B3%B4%EB%93%9C/more/flea_market?page=" + str(num)
    carrot_res = req.get(carrot_url)

    carrot_soup = BS(carrot_res.text, "html.parser")
    carrot_data = carrot_soup.select("article")

    if len(carrot_data) <= 1:
        global result
        result = 1
    else:
        for carrot_datum in carrot_data:
            carrot_product_image = carrot_datum.select_one("a > div.card-photo > img")
            carrot_product_title = carrot_datum.select_one("a > div.article-info > div > span.article-title").text
            carrot_product_price = carrot_datum.select_one("a > div.article-info > p.article-price").text
            carrot_product_loca = carrot_datum.select_one("a > div.article-info > p.article-region-name").text
            carrot_product_url_tail = carrot_datum.select_one("a")["href"]
            # ProductPageLink Scraping
            carrot_product_url = carrot_main_url + carrot_product_url_tail
            carrot_product_res = req.get(carrot_product_url)
            carrot_product_soup = BS(carrot_product_res.text, "html.parser")
            carrot_product_time = carrot_product_soup.select_one("#article-category > time").text
            carrot_product_category = carrot_product_soup.select_one("#article-category > time").previous_sibling.text

            print(carrot_product_image, carrot_product_title, carrot_product_price, carrot_product_loca,  carrot_product_url, carrot_product_category,        carrot_product_time)

    # if len(carrot_data) <= 1:
    #     global result
    #     result = 1
    # else:
    #     for carrot_datum in carrot_data:
    #         product_image_carrot = carrot_datum.select_one("a > div.card-photo > img")
    #         product_title_carrot = carrot_datum.select_one("a > div.article-info > div > span.article-title").text
    #         product_price_carrot = carrot_datum.select_one("a > div.article-info > p.article-price").text
    #         product_loca_carrot = carrot_datum.select_one("a > div.article-info > p.article-region-name").text
    #         print(product_image_carrot, product_title_carrot, product_price_carrot, product_loca_carrot)


# t1 = time.perf_counter()

# threads = []
# i = 800

# #동시에 doodle 함수 실행
# while 1:
#     i += 1
#     if result == 1:
#         break
#     t = Thread(target=carrot_scrap, args=[i])
#     t.start()
#     threads.append(t)
    
# for thread in threads:
#     thread.join()
# t2 = time.perf_counter()

# print(f'Finished in {round(t2-t1, 2)} second(s)')

carrot_scrap(1)

