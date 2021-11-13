from bs4 import BeautifulSoup as BS
import requests as req


carrot_result = 0


def carrot_scrap(word, num):
    carrot_url_head = "https://www.daangn.com"
    carrot_url = f"{carrot_url_head}/search/{word}/more/flea_market?page={str(num)}"
    carrot_res = req.get(carrot_url)
    carrot_soup = BS(carrot_res.text, "html.parser")
    carrot_data = carrot_soup.select("article")

    cards = []

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
                "a > div.article-info > p.article-price").text
            carrot_product_loca = carrot_datum.select_one(
                "a > div.article-info > p.article-region-name").text
            carrot_product_url_tail = carrot_datum.select_one("a")["href"]
            # ProductPageLink Scraping
            carrot_product_url = carrot_url_head + carrot_product_url_tail
            carrot_product_res = req.get(carrot_product_url)
            carrot_product_soup = BS(carrot_product_res.text, "html.parser")
            carrot_product_time = carrot_product_soup.select_one(
                "#article-category > time").text
            carrot_product_category = carrot_product_soup.select_one(
                "#article-category > time").previous_sibling.text

            card = {'url': carrot_product_url, 'title': carrot_product_title,
                    'image': carrot_product_image, 'price': carrot_product_price, 'location': carrot_product_loca, 'time': carrot_product_time, 'category': carrot_product_category}
            cards.append(card)
    return cards

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
print(carrot_scrap("아이패드", 1))
