from bs4 import BeautifulSoup
import requests
import time
import random
from db_auto import db, cursor


def fetch_car_data(url):
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    return html_soup.find_all('div', class_="content-bar")


def save_to_database(title, price, url_auto_ria):
    cursor.execute('SELECT * FROM auto WHERE url_auto_ria = ?', (url_auto_ria,))
    existing_data = cursor.fetchone()
    if existing_data:
        print('Ці дані про авто вже в базі')
    else:
        cursor.execute('INSERT INTO auto (marka_auto, price, url_auto_ria) VALUES (?, ?, ?)',
                       (title, price, url_auto_ria))
        db.commit()
        print(f'{title} => {price}$ url => {url_auto_ria}')


def main():
    cars = []
    count = 1

    while count <= 2:
        url = f'https://auto.ria.com/uk/search/?indexName=auto&categories.main.id=1&brand.id[0]=79&model.id[' \
              f'0]=2104&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&confiscated=0&credit=0&page=0' \
              f'{count}'
        cars_data = fetch_car_data(url)
        if cars_data:
            cars.extend(cars_data)
            value = random.uniform(5, 9)
            time.sleep(value)
        else:
            print('empty')
            break
        count += 1

    for car in cars:
        info = car
        title = info.find('a', {"class": "address"}).text
        price = info.find('span', {"class": "bold size22 green"}).text
        url_auto_ria = info.find('a', {"class": "address"})['href']
        save_to_database(title, price, url_auto_ria)


if __name__ == "__main__":
    while True:
        main()
        # затримка 10 хв
        time.sleep(600)
