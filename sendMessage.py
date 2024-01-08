import requests
from db_auto import db, cursor
from datetime import datetime


# Ваш токен бота
bot_token = '1334679162:AAEU9PnLglkVWm7B2swd_V3KbrkN1QAH3XA'

# ID чату, куди ви хочете надіслати повідомлення
chat_id = '-1002040915824'


cursor.execute('SELECT * FROM auto')
rows = cursor.fetchall()
# print(rows)


# URL для взаємодії з Telegram Bot API
url_tg = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}'

for row in rows:
    # print(row[-1])
    # Параметри запиту
    params = {
        'text': f'Знайдено машину для вас {row[1]} ціна {row[2]}$  посилання\n => {row[3]}'
    }
    # перевірка чи є такий пост в каналі через db
    cursor.execute('SELECT * FROM tg_post WHERE url_auto_ria = ?', (row[-1],))
    tg_url_post = cursor.fetchone()

    if tg_url_post:
        print('Ці дані про авто вже в каналі')
    else:
        # Запис даних в таблицю tg_post
        current_time = datetime.now()
        cursor.execute('INSERT INTO tg_post (time_stamp, url_auto_ria) VALUES (?, ?)', (current_time, row[-1]))
        db.commit()

        # Відправка POST-запиту
        response = requests.post(url_tg, params=params)

        # Перевірка статусу відповіді
        if response.status_code == 200:
            print('Повідомлення успішно надіслано')
        else:
            print(f'Помилка {response.status_code}: {response.text}')
