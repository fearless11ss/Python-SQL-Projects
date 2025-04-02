# В данном коде реализован базовый функционал регистрации + авторизации с помощью Python+SQL

import sqlite3


# создание и подключение к базе данных
db = sqlite3.connect("registration.db")
cur = db.cursor()

# создание таблицы users_data
cur.execute("""CREATE TABLE IF NOT EXISTS users_data(
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Login TEXT NOT NULL,
                Password TEXT NOT NULL,
                Code TEXT NOT NULL);""")

# добавление данных из пункта задания 3
# cur.execute("""INSERT INTO users_data(UserID, Login, Password, Code)
#             VALUES (1, 'Ivan', 'qwer1234', '1234');""")
# db.commit()

# основная часть программы
while True:
    print("Выберите необходимое действие(регистрация - 1, авторизация - 2, восстановление пароля по коду - 3, выход из программы - 4):")

    # выбор пользователем необходимого ему действия
    choose = input()
    if choose!="1" and choose!='2' and choose!='3' and choose!='4':
        print("Введено некорректное значение")
        continue

    # код модуля регистрации
    if choose == '1':
        print("Придумайте новый логин:")
        new_login = input().lower()
        if len(new_login) == 0:
            print("Ошибка регистрации, логин не может быть пустым полем")
            continue
        cur.execute("""SELECT Login FROM users_data WHERE LOWER(Login) = ?;""", (new_login, ))
        result = cur.fetchall()
        if result:
            print("Ошибка регистрации, такой логин уже существует")
            continue
        print("Придумайте новый пароль")
        new_pass = input()
        if len(new_pass) == 0:
            print("Ошибка регистрации, пароль не может быть пустым полем")
            continue
        print("Придумайте 4-х значный цифровой код для восстановления пароля")
        new_code = input()
        if len(new_code) != 4 or not new_code.isdigit():
            print("Ошибка регистрации, придумайте корректный код")
            continue
        cur.execute("""INSERT INTO users_data(Login, Password, Code)
                    VALUES (?, ?, ?);""", (new_login, new_pass, new_code))
        db.commit()
        print("Успешная регистрация!")

    # код модуля авторизации
    if choose == '2':
        print("Введите логин:")
        login = input().lower()
        if len(login) == 0:
            print("Ошибка авторизации, вы не ввели логин")
            continue
        cur.execute("""SELECT Login FROM users_data WHERE LOWER(Login) = ?;""", (login,))
        result = cur.fetchall()
        if result:
            print("Введите пароль:")
            password = input()
            if len(password) == 0:
                print("Ошибка авторизации, вы не ввели пароль")
                continue
            cur.execute("""SELECT Password FROM users_data WHERE LOWER(Login) = ? AND Password = ?;""", (login, password))
            result = cur.fetchall()
            if result:
                print("Успешная авторизация!")
            else:
                print("Ошибка авторизации, введен неверный пароль")
                continue
        else:
            print("Ошибка авторизации, такого логина не существует")
            continue

    # код модуля восстановления пароля по коду
    if choose == '3':
        print("Введите свой логин:")
        login = input().lower()
        if len(login) == 0:
            print("Ошибка восстановления пароля, вы не ввели логин")
            continue
        cur.execute("""SELECT Login FROM users_data WHERE LOWER(Login) = ?;""", (login,))
        result = cur.fetchall()
        if result:
            print("Введите код для восстановления пароля:")
            code = input()
            cur.execute("""SELECT Code FROM users_data WHERE LOWER(Login) = ? AND Code = ?;""", (login, code))
            result = cur.fetchall()
            if result:
                print("Придумайте новый пароль:")
                password = input()
                if len(password) == 0:
                    print("Ошибка смены пароля, вы не ввели пароль")
                    continue
                cur.execute("""UPDATE users_data SET Password = ? WHERE LOWER(Login) = ? AND Code = ?;""", (password, login, code))
                db.commit()
                print("Пароль изменен успешно!")
            else:
                print("Ошибка восстановления пароля, введен неверный код")
                continue
        else:
            print("Ошибка восстановления пароля, такого логина не существует")
            continue

    # код модуля выхода из программы
    if choose == '4':
        print("Выход из программы")
        break
