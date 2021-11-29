from bs4 import BeautifulSoup as BS
import requests as req
from threading import Thread
import time


carrot_result = 0


def carrot_page(d, word, num):
    page = []
    carrot_url_head = "https://www.daangn.com"
    carrot_url = f"{carrot_url_head}/search/{word}/more/flea_market?page={str(num)}"
    carrot_res = req.get(carrot_url)
    carrot_soup = BS(carrot_res.text, "html.parser")
    carrot_data = carrot_soup.select("article")

    if len(carrot_data) <= 1:
        global carrot_result
        carrot_result = 1
    else:
        for carrot_datum in carrot_data:
            carrot_product_image = carrot_datum.select_one(
                "a > div.card-photo > img")
            carrot_product_title = carrot_datum.select_one(
                "a > div.article-info > div > span.article-title").text
            carrot_product_price = carrot_datum.select_one(
                "a > div.article-info > p.article-price").text.strip()
            carrot_product_loca = carrot_datum.select_one(
                "a > div.article-info > p.article-region-name").text.strip()
            carrot_product_url_tail = carrot_datum.select_one("a")["href"]
            carrot_product_url = carrot_url_head + carrot_product_url_tail
            carrot_product_res = req.get(carrot_product_url)
            carrot_product_soup = BS(
                carrot_product_res.text, "html.parser")
            carrot_product_time = carrot_product_soup.select_one(
                "#article-category > time").text.strip()
            carrot_product_category = carrot_product_soup.select_one(
                "#article-category > time").previous_sibling.text.strip()

            card = {'url': carrot_product_url, 'title': carrot_product_title,
                    'image': carrot_product_image, 'price': carrot_product_price, 'location': carrot_product_loca, 'time': carrot_product_time, 'category': carrot_product_category}
            page.append(card)
        d[num] = page
    return

# def carrot(word):
#     threads = []
#     i = 800
#     while True:
#         i += 1
#         global carrot_result
#         if carrot_result == 1:
#             break
#         t = Thread(target=carrot_page, args=(word, i))
#         t.start()
#         threads.append(t)

#     for thread in threads:
#         thread.join()

#####


def carrot(word):
    lala = {}
    threads = []
    for i in range(3):
        t = Thread(target=carrot_page, args=(lala, word, i))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    return lala


t1 = time.perf_counter()
pages = {}
for i in range(3):
    carrot_page(pages, "화이트보드", i)
print(pages)
t2 = time.perf_counter()
print(f'Finished in {round(t2-t1, 2)} second(s)')


t3 = time.perf_counter()
print(carrot("화이트보드"))
t4 = time.perf_counter()
print(f'Finished in {round(t4-t3, 2)} second(s)')

#####

# print(cards)
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

# print(f'Finished in {round(t2-t1, 2)} second(s)'
