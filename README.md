Scraping Auto Ria

Проект "Scraping_auto_ria" - це інструмент, який використовує веб-скрапінг для отримання інформації про автомобілі з 
сайту Auto Ria.

Опис
1. Цей проект надає можливість отримувати дані про автомобілі з веб-сайту Auto Ria. Ви можете використовувати його для 
отримання оновленої інформації про авто, такої як модель, рік випуску, ціна, тощо.

Властивості
2. Веб-скрапінг Auto Ria: Проект скрапить дані з веб-сайту Auto Ria та зберігає їх для подальшого використання.

Використання
Встановлення залежностей:

pip install -r requirements.txt

Запуск скрапінгу:

Створіть таблицю в базі даних запустивши файл => db_auto.py

python scraper.py
Скрапер отримає дані з Auto Ria та збереже їх у файл output.csv.


Відправка у Telegram:

Вкажіть свій токен та чат ID у файлі config.py.

python
Copy code
# sendMessage.py
TELEGRAM_TOKEN = 'your_telegram_token'
TELEGRAM_CHAT_ID = 'your_chat_id'

Використовуйте отримані дані для своїх потреб. Ви можете використовувати збережені CSV-файли або інтегрувати їх у свої проекти.
