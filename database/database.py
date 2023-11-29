import logging
import sqlite3
import json

logging.basicConfig(filename='database.log', level=logging.INFO)


def create_table():
    """
        Создает таблицу в базе данных SQLite, если она не существует

        Данная функция подключается к базе данных SQLite и создает таблицу с именем 'users' со следующими столбцами:
        - id: INTEGER (первичный ключ)
        - first_name: TEXT
        - last_name: TEXT
        - history: TEXT
        - favorite: TEXT
    """
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    history TEXT DEFAULT None,
                    favorite TEXT DEFAULT None
                )
            ''')
            conn.commit()
            logging.info('Таблица "users" успешно создана')
    except Exception as e:
        logging.error(f'Ошибка при создании таблицы "users": {str(e)}')


def insert_user(user_id: int, first_name: str, last_name: str, history: str = None, favorite: str = None):
    """
        Вставляет данные пользователя в таблицу 'users'.

        Данная функция вставляет новую запись в таблицу 'users' с предоставленной информацией о пользователе.

        Параметры:
        - user_id: ID пользователя (целое число).
        - first_name: Имя пользователя (строка).
        - last_name: Фамилия пользователя (строка).
        - history: История запросов.
        - favorite: Сохраненные рецепты.
    """
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()

            c.execute('SELECT history FROM users WHERE id = ?', (user_id,))
            result = c.fetchone()

            if result is not None:
                history_list = json.loads(result[0])
            else:
                history_list = []
            if len(history_list) >= 11:
                history_list.pop(0)
            if history is not None:
                history_list.append(history)
            history_str = json.dumps(history_list, ensure_ascii=False)

            c.execute('SELECT favorite FROM users WHERE id = ?', (user_id,))
            result = c.fetchone()

            if result is not None:
                favorite_list = json.loads(result[0])
            else:
                favorite_list = []
            if favorite is not None and favorite not in favorite_list:
                favorite_list.append(favorite)
            favorite_str = json.dumps(favorite_list, ensure_ascii=False)

            c.execute('''
                            INSERT OR REPLACE INTO users (id, first_name, last_name, history, favorite)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (user_id, first_name, last_name, history_str, favorite_str))
            conn.commit()
            logging.info(f'Пользователь с ID {user_id} успешно добавлен в таблицу "users"')
    except Exception as e:
        logging.error(f'Ошибка при добавлении пользователя в таблицу "users": {str(e)}')


def get_user(user_id: int) -> tuple:
    """
        Получает данные пользователя из таблицы 'users'.

        Данная функция извлекает данные пользователя с указанным ID из таблицы 'users'.

        Параметры:
        - user_id: ID пользователя (целое число).

        Возвращает:
        - user_data: Кортеж, содержащий данные пользователя, полученные из таблицы 'users'.
    """
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user_data = c.fetchone()
            if user_data:
                logging.info(f'Данные пользователя с ID {user_id} успешно получены')
            else:
                logging.warning(f'Пользователь с ID {user_id} не найден')
            return user_data
    except Exception as e:
        logging.error(f'Ошибка при получении данных пользователя: {str(e)}')


def update_favorite_user(user_id: int, favorite: str):
    """
        Обновляет поле favorite пользователя в таблице 'users'.

        Данная функция обновляет поле favorite пользователя с указанным ID в таблице 'users'.

        Параметры:
        - user_id: ID пользователя (целое число).
        - favorite: Новое значение поля favorite (строка).
    """
    try:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()

            c.execute('UPDATE users SET favorite = ? WHERE id = ?', (favorite, user_id))
            conn.commit()
            logging.info(f'Поле favorite пользователя с ID {user_id} успешно обновлено')
    except Exception as e:
        logging.error(f'Ошибка при обновлении поля favorite пользователя: {str(e)}')
