import sqlite3
db = sqlite3.connect("auto.db")

cursor = db.cursor()

# Створення таблиці "машини"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS auto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marka_auto TEXT,
        price BIGINT,
        url_auto_ria TEXT
           
 )''')

db.commit()
