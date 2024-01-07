from bs4 import BeautifulSoup  # для парсинга старниц
import requests  # для запросов к сайту, получения содержимого веб-страницы
from requests import get
import time
import random
from db_auto import db, cursor

# # Запуск перевірки кожні 10 хвилин у циклі while
# while True:
#     check_resource() Виконання основного коду в тілі циклу
#
#     # Затримка на 10 хвилин
#     time.sleep(600)
#

houses = []
count = 1
while count <= 3:
    url = 'https://auto.ria.com/uk/search/?indexName=auto&categories.main.id=1&brand.id[0]=79&model.id[' \
          '0]=2104&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&confiscated=0&credit=0&page=0' \
          '' + str(count)
    # print(url)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    house_data = html_soup.find_all('div', class_="content-bar")
    if house_data:
        # Робимо затримку під час запити, щоб сайт не заблокував нас
        houses.extend(house_data)
        value = random.random()
        scaled_value = 1 + (value * (9 - 5))
        # print(scaled_value)
        time.sleep(scaled_value)
    else:
        print('empty')
        break
    count += 1

n = int(len(houses)) - 1
count = 0
while count <= n:  # count <= n
    info = houses[int(count)]
    title = info.find('a', {"class": "address"}).text
    price = info.find('span', {"class": "bold size22 green"}).text
    url_auto_ria = info.find('a', {"class": "address"})['href']
    # Перевірка чи є ці вже дані в базі
    cursor.execute('SELECT * FROM auto WHERE url_auto_ria = ?', (url_auto_ria,))
    existing_data = cursor.fetchone()
    if existing_data:
        print('Ці дані про авто вже в базі')
    else:
        cursor.execute('''
            INSERT INTO auto (marka_auto, price, url_auto_ria) VALUES (?, ?, ?)
        ''', (title, price, url_auto_ria))
        db.commit()
        print(f'{title} => {price}$ url => {url_auto_ria}')
    count += 1

