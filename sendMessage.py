import requests
from db_auto import db, cursor
from datetime import datetime
import time


def send_telegram_message(bot_token, chat_id, text):
    url_tg = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}'
    params = {'text': text}
    response = requests.post(url_tg, params=params)

    if response.status_code == 200:
        print('Повідомлення успішно надіслано')
    else:
        print(f'Помилка {response.status_code}: {response.text}')


def main():
    bot_token = ''
    chat_id = ''

    cursor.execute('SELECT * FROM auto')
    rows = cursor.fetchall()

    for row in rows:
        cursor.execute('SELECT * FROM tg_post WHERE url_auto_ria = ?', (row[-1],))
        tg_url_post = cursor.fetchone()

        if tg_url_post:
            print('Ці дані про авто вже в каналі')
        else:
            # Запис даних в таблицю tg_post
            try:
                current_time = datetime.now()
                cursor.execute('INSERT INTO tg_post (time_stamp, url_auto_ria) VALUES (?, ?)', (current_time, row[-1]))
                db.commit()
            except sqlite3.IntegrityError:
                print(f'Дані про авто з url {row[-1]} вже існують в базі')
            text = f'Знайдено машину для вас Держ номер {row[4]} {row[1]} ціна {row[2]}$  посилання\n => {row[3]}'
            send_telegram_message(bot_token, chat_id, text)


if __name__ == "__main__":
    while True:
        try:

            main()
            # Затримку на випадок повторення
            time.sleep(100)
        except KeyboardInterrupt:
            print('Виконання програми перервано користувачем.')

