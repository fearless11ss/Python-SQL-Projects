# В данном задании необходимо было объявить пользователя и тарифы на звонки на других операторов, и реализовать работу 30 звонков (один звонок в день на случайного оператора)

# импорт необходимых библиотек
import random
import csv
import sqlite3
import datetime

# функции для работы с csv-файлом
def create_report_file():
    data = [
        ("Date", "Operator", "Count_min", "Amount")
    ]
    with open("report_mobile.csv", "a", newline='') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(
                data
            )
def report_operation(date, operator, count_min, amount):
    user_data = [
        (date, operator, count_min, amount)
    ]
    with open("report_mobile.csv", "a", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(
            user_data
        )

# подключение к базе данных
db = sqlite3.connect("mobile_calls.db")
cur = db.cursor()

# создание таблиц
cur.execute("""CREATE TABLE IF NOT EXISTS mobile_users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            User TEXT NOT NULL,
            Balance INTEGER NOT NULL)""")
db.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS mobile_price (
            PriceID INTEGER PRIMARY KEY AUTOINCREMENT,
            Mts_Mts INTEGER NOT NULL,
            Mts_Tele2 INTEGER NOT NULL,
            Mts_Yota INTEGER NOT NULL)""")
db.commit()

# заполнение таблиц
cur.execute("""INSERT INTO mobile_users (User, Balance) VALUES ("User1", 500)""")
db.commit()
cur.execute("""INSERT INTO mobile_price (Mts_Mts, Mts_Tele2, Mts_Yota) VALUES (1, 2, 3)""")
db.commit()

# основная логика
create_report_file()
cur.execute("""SELECT Mts_Mts, Mts_Tele2, Mts_yota FROM mobile_price;""")
operator_info = cur.fetchone()
for i in range(1, 31):
    now_date = datetime.datetime.utcnow().strftime("%H:%M-%d.%m.%Y")
    operator = random.choice(operator_info)
    mins_amount = random.randint(1, 10)
    cur.execute("""SELECT Balance FROM mobile_users WHERE User = "User1";""")
    result = cur.fetchone()
    balance = result[0]
    price = operator * mins_amount
    if balance < price:
        print(f"Звонок №{i}: неудачная попытка списания {price} рублей при звонке на оператора {operator} длительностью {mins_amount} минут(-ы). Баланс пользователя - {balance}")
        continue
    cur.execute(f"""UPDATE mobile_users SET Balance = {balance-price} WHERE User = "User1";""")
    db.commit()
    print(f"Звонок №{i}: успешное списание {price} рублей при звонке на оператора {operator} длительностью {mins_amount} минут(-ы). Баланс пользователя - {balance}")
    report_operation(now_date, operator, mins_amount, price)

# закрытие подключения к базе данных
db.close()
