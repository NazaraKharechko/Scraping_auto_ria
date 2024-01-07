import requests
from db_auto import db, cursor

# Ваш токен бота
bot_token = '1334679162:AAEU9PnLglkVWm7B2swd_V3KbrkN1QAH3XA'

# ID чату, куди ви хочете надіслати повідомлення
chat_id = '-1002040915824'


cursor.execute('SELECT * FROM auto')
rows = cursor.fetchall()

# URL для взаємодії з Telegram Bot API
url_tg = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}'

for row in rows:
    print(row)
    # Параметри запиту
    params = {
        'text': f'Знайдено машину для вас {row[1]} ціна {row[2]}$  посилання\n => {row[3]}'
    }

    # Відправка POST-запиту
    response = requests.post(url_tg, params=params)

    # Перевірка статусу відповіді
    if response.status_code == 200:
        print('Повідомлення успішно надіслано')
    else:
        print(f'Помилка {response.status_code}: {response.text}')
