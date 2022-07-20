'''Скрипт работы с СУБД PostgreSQL'''
import datetime
import time
import psycopg2.extras

from sup_data_process import main

# configs (вводим свои настройки)
HOST = "127.0.0.1"
PORT = '5432'
USER = "postgres"
PASSWORD = "1"
DB = "postgres"

# Сообщения процесса
DUMP_MSG = "[INFO] Table dumped successfully"
TABLE_CREATE_MSG = "[INFO] Table created successfully"
INSERT_MSG = "[INFO] Data was succefully inserted"
EXCEPTION_MSG = "[INFO] Error while working with PostgreSQL"
CON_CLOSE_MSG = "[INFO] PostgreSQL connection closed"

# Интервал между обновлениями БД, сек.
interval = 300


def connection():
    return psycopg2.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB)


connect = None
# Создаем резервную копию
try:
    connect = connection()
    with connect.cursor() as cursor:
        cursor.execute('SELECT * FROM supplies')
        with open(f"supplies_dump_{datetime.datetime.now().date()}.sql", 'w') as f:
            for row in cursor:
                f.write("INSERT INTO supplies VALUES (" + str(row) + ");")
    print(DUMP_MSG)
except Exception as _ex:
    print(EXCEPTION_MSG, _ex)
finally:
    if connect:
        connect.close()
        print(CON_CLOSE_MSG)

# Основной цикл программы
while True:
    # Запрашиваем обновленные данные
    args = main()
    try:
        # Подключаемся к базе данных
        connect = connection()
        # Включаем автоматические коммиты
        connect.autocommit = True

        # Далее используем cursor и менеджер контекста для выполнения операций с базой данных

        # create a new table
        with connect.cursor() as cursor:
            cursor.execute(
                '''DROP TABLE IF EXISTS supplies;
                CREATE TABLE supplies(
                supply_id serial PRIMARY KEY,
                supply_num INT,
                cost_usd NUMERIC,
                terms DATE,
                cost_rub NUMERIC);'''
            )
            print(TABLE_CREATE_MSG)

        # insert data into a table
        with connect.cursor() as cursor:
            insert_query = 'INSERT INTO supplies (supply_id, supply_num, cost_usd, terms, cost_rub) ' \
                           'VALUES %s'
            psycopg2.extras.execute_values(
                cursor, insert_query, args, template=None
            )
            print(INSERT_MSG)

        # # to check: get data from a table
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         """SELECT * FROM supplies WHERE supply_id = '1';"""
        #     )
        #     print(cursor.fetchone())

    except Exception as _ex:
        print(EXCEPTION_MSG, _ex)
    finally:
        if connect:
            connect.close()
            print(CON_CLOSE_MSG)

    # Ждём заданный интервал времени
    time.sleep(interval)
