import sqlite3

#Подключение к базе данных
connection = sqlite3.connect('tg_bot.db', check_same_thread=False)
#Связь между Python и SQL
sql = connection.cursor()

#Создание таблицы пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(id INTEGER,'
            'name TEXT,'
            'number TEXT,'
            'location TEXT);')
#Создание таблицы продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products'
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'pr_name TEXT,'
            'pr_amount INTEGER,'
            'pr_price REAL,'
            'pr_des TEXT,'
            'pr_photo TEXT);')
#Создание таблицы корзины пользователя
sql.execute('CREATE TABLE IF NOT EXISTS user_cart'
            '(user_id INTEGER,'
            'user_product TEXT,'
            'product_quantity INTEGER,'
            'total REAL);')

##Методы для пользователя##

#Регистрация
def register(id, name, number, location):
    sql.execute('INSERT INTO users VALUES (?, ?, ?, ?);',
                (id, name, number, location))
    #Фиксируем изменения
    connection.commit()

#Проверка на регистрацию
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;',
                        (id,))

    if check.fetchone():
        return True
    else:
        return False

##Методы для продуктов##
#Вывод информации о конкретном продукте
def show_info(pr_name):
    sql.execute('SELECT pr_name, pr_des,'
                'pr_amount, pr_price, '
                'pr_photo WHERE pr_name=?;', (pr_name,)).fetchone()

#Добавление товаров
def add_product(pr_name, pr_amount, pr_price, pr_des, pr_photo):
    sql.execute('INSERT INTO products (pr_name,'
                'pr_amount,'
                'pr_price,'
                'pr_des,'
                'pr_photo) VALUES (?, ?, ?, ?, ?);',
                (pr_name, pr_amount, pr_price, pr_des, pr_photo))
    #Фиксируем изменения
    connection.commit()

#Вывод всех продуктов из базы
def get_all_products():
    all_products = sql.execute('SELECT * FROM products;')

    return all_products.fetchall()

#Вывод id товаров
def get_pr_name_id():
    products = sql.execute('SELECT pr_id,'
                           'pr_name,'
                           'pr_amount FROM products;').fetchall()

    return products

def get_pr_id():
    prods = sql.execute('SELECT pr_name, pr_id, pr_amount FROM products;').fetchall()
    sorted_prods = [i[1] for i in prods if i[2] > 0]
    return sorted_prods


##Методы для корзины##
#Добавление в корзину
def add_to_cart(user_id, user_pr, pr_quantity, user_total=0):
    sql.execute('INSERT INTO user_cart VALUES (?, ?, ?, ?);',
                (user_id, user_pr, pr_quantity, user_total))
    #Фиксируем изменения
    connection.commit()

#Удаление из корзины
def del_from_cart(user_id):
    sql.execute('DELETE FROM user_cart WHERE user_id=?;', (user_id,))
    #Фиксируем изменения
    connection.commit()

#Отображение корзины
def show_cart(user_id):
    cart = sql.execute('SELECT user_product,'
                'product_quantity,'
                'total FROM user_cart WHERE user_id=?;', (user_id,)).fetchone()
    return cart

# def get_exact_user_cart(user_id):
#     user_cart = sql.execute('SELECT')
# def r():
#     sql.execute('INSERT INTO products (pr_name, pr_amount, pr_price, pr_des, pr_photo)'
#                 'VALUES ("лаваш", 120, 22000.0, "оч вкусно", '
#                 '"https://i.postimg.cc/pLnjprK6/da9581ee81134ea59740836aaf9e4a57-e1580887902436.jpg");')
#
#     connection.commit()
# r()