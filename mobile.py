# В данном задании реализовывался функционал списания абонентской платы в заданный пользователем период дней.
# Имеется несколько пользователей, все они пользуются разными тарифами

# создание и подключение к базе данных
import sqlite3
db = sqlite3.connect("mobile.db")
cur = db.cursor()

# создание таблиц базы данных
cur.execute("""CREATE TABLE IF NOT EXISTS mobile_users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_name TEXT NOT NULL,
            Balance INTEGER NOT NULL,
            Mobile_tariff_ref INTEGER NOT NULL,
            Activity TEXT NOT NULL)""")
db.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS mobile_tariff (
            TariffID INTEGER PRIMARY KEY AUTOINCREMENT,
            Tariff TEXT NOT NULL,
            Price INTEGER NOT NULL)""")
db.commit()

# заполнение таблиц базы данных
cur.execute("""INSERT INTO mobile_users(User_name, Balance, Mobile_tariff_ref, Activity)
            VALUES
            ("User1", 10000, 2, "Yes"),
            ("User2", 10000, 3, "Yes"),
            ("User3", 10000, 1, "Yes")""")
db.commit()
cur.execute("""INSERT INTO mobile_tariff(Tariff, Price)
            VALUES
            ("Standart", 500),
            ("VIP", 1000),
            ("Premium", 1500)""")
db.commit()

while True:
    period = input("Введите период расчета в месяцах:")
    try:
        period = int(period)
        if period <= 0:
            raise ValueError
        break
    except ValueError:
        print("Ошибка, введено некорректное значение")
cur.execute("""SELECT * FROM mobile_users;""")
users_data = cur.fetchall()
cur.execute("""SELECT * FROM mobile_tariff;""")
tariff_data = cur.fetchall()
for j in range(1, period+1):
    print(f"Месяц №{j}")
    for i in range(len(users_data)):
        cur.execute(f"""SELECT Activity FROM mobile_users WHERE UserID = {users_data[i][0]}""")
        result = cur.fetchone()
        status = result[0]
        cur.execute(f"""SELECT Mobile_tariff_ref FROM mobile_users WHERE UserID = {users_data[i][0]}""")
        result = cur.fetchone()
        tariff_id = result[0]
        cur.execute(f"""SELECT Price FROM mobile_tariff WHERE TariffID = {tariff_id}""")
        result = cur.fetchone()
        price = result[0]
        cur.execute(f"""SELECT Balance FROM mobile_users WHERE UserID = {users_data[i][0]}""")
        result = cur.fetchone()
        balance = result[0]
        if status == "No":
            print(f"{users_data[i][1]} недостаточно средств на балансе. Баланс пользователя - {balance}")
            continue
        if balance < price:
            print(f"{users_data[i][1]} недостаточно средств на балансе. Баланс пользователя - {balance}")
            cur.execute(f"""UPDATE mobile_users SET Activity = "No" WHERE UserID = {users_data[i][0]};""")
            continue
        cur.execute(f"""UPDATE mobile_users SET Balance = {balance-price} WHERE UserID = {users_data[i][0]}""")
        db.commit()
        print(f"{users_data[i][1]} списание {price} рублей. Остаток - {balance-price}")
# закрытие подключения к базе данных
db.close()
