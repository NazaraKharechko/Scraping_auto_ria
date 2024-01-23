from datetime import datetime
from bs4 import BeautifulSoup
import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from db_auto import db, cursor


def fetch_car_data(url):
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    return html_soup.find_all('div', class_="content-bar")


def save_to_database(title, price, url_auto_ria, car_number, car_vin):
    cursor.execute('SELECT * FROM auto WHERE url_auto_ria = ?', (url_auto_ria,))
    existing_data = cursor.fetchone()
    if existing_data:
        print('Ці дані про авто вже в базі')
    else:
        cursor.execute('INSERT INTO auto (marka_auto, price, url_auto_ria, car_number, car_vin) VALUES (?, ?, ?, ?, ?)',
                       (title, price, url_auto_ria, car_number, car_vin))
        db.commit()
        print(f'{title} => {price}$ url => {url_auto_ria} => car_number {car_number} car_vin => {car_vin}')


def main():
    """Завдаємо пошук авто по параметрах і ск сторінок робити скрапінг """
    cars = []
    count = 1

    while count <= 4:
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

        # Знаходимо елементи для номера автомобіля і VIN-коду
        car_number_element = info.find('span', class_='state-num ua')
        vin_element = info.find('span', class_='label-vin')

        # Отримуємо текст з елементів
        car_number = car_number_element.text.strip()[:10] if car_number_element else None
        car_vin = vin_element.find('span').text.strip() if vin_element else None

        save_to_database(title, price, url_auto_ria, car_number, car_vin)


def get_all_data_of_car():
    """Пошук даних про конкпетре авто з наших всіх авто в пошуку"""
    cursor.execute('SELECT * FROM auto')
    rows = cursor.fetchall()
    for row in rows:
        driver = webdriver.Chrome()
        # Отримати HTML-код з вказаного URL
        url = row[3]
        response = requests.get(url)
        html_code = response.text
        # Створити об'єкт BeautifulSoup
        soup = BeautifulSoup(html_code, 'html.parser')

        title_car = soup.find('h1', {"class": "head"}).text
        price_usd = soup.find('div', {"class": "price_value"}).text
        odometer = soup.find('span', {"class": "size18"}).text
        username = soup.find('div', {"class": "seller_info_name bold"}).text

        driver.get(row[3])
        # Знаходимо елемент "показати" і клікаємо на нього
        show_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "показати")))
        show_button.click()
        # Знаходимо елемент із номером телефону після кліку
        phone_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "list-phone"))
        )
        # Отримуємо  номер телефону
        phone_number = phone_element.text[-15:]
        # Закриваємо веб-драйвер
        driver.quit()

        image_url = soup.find('img', {"class": "outline m-auto"})['src']
        images_count = soup.find('span', {"class": "count"}).text
        datetime_found = datetime.now()

        # Знаходимо елементи для номера автомобіля і VIN-коду
        car_number_element = soup.find('span', class_='state-num ua')
        vin_element = soup.find('span', class_='label-vin')

        # Отримуємо текст з елементів
        car_number = car_number_element.text.strip()[:10] if car_number_element else None
        car_vin = vin_element.text.strip() if vin_element else None
        print(f'1{url} 2{title_car} 3{price_usd}$ 4{odometer}000 Owner{username} Phone{phone_number} Img_url{image_url}'
              f'Img_count{images_count[3:6]} data{datetime_found} Car number => {car_number} vin => {car_vin}')


if __name__ == "__main__":
    while True:
        main()
        get_all_data_of_car()
        # затримка 10 хв
        time.sleep(600)
