import sqlite3
db = sqlite3.connect("auto.db")

cursor = db.cursor()

try:
    # Створення таблиці "машини"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marka_auto TEXT,
            price BIGINT,
            url_auto_ria TEXT
     )''')

    # Створення таблиці дані про пост в каналі
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tg_post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            url_auto_ria TEXT
     )''')

    db.commit()
except sqlite3.Error as e:
    print(f"Помилка SQLite: {e}")

# # Виконання запиту для виведення всіх даних з таблиці
# cursor.execute("SELECT * FROM auto;")
#
# # Отримання результатів
# data = cursor.fetchall()
#
# # Виведення даних
# print("Дані з таблиці:")
# for row in data:
#     print(row)
