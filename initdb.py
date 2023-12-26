import csv

import mysql.connector

MYSQL_USERNAME = 'gameapp'
MYSQL_PASS = 'gameappt0lk2o20'
MYSQL_PORT = 3308
MYSQL_HOST = '5.34.200.127'
MYSQL_DB = 'gameapp_db'
MYSQL_TABLE_NAME = 'laptops'

connection = mysql.connector.connect(
    user=MYSQL_USERNAME,
    password=MYSQL_PASS,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DB
)


def clear_db():
    cursor = connection.cursor()
    cursor.execute('DELETE FROM gameapp_db.laptops')
    cursor.close()
    connection.commit()
    print(cursor.rowcount, "record(s) deleted")


def insert_into_db(laptops):
    cursor = connection.cursor()
    sql = f"INSERT INTO {MYSQL_TABLE_NAME} (id, price, cpu, ram, ssd, graphic, screen_size, hdd, company, redirect_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = [(int(laptop['index']) + 1, laptop['price'], laptop['cpu'], laptop['ram'], laptop['ssd'],
            laptop['graphic_ram'], laptop['screen_size'], laptop['hdd'], laptop['company'], laptop['links']) for laptop in laptops]
    cursor.executemany(sql, val)
    connection.commit()
    print(cursor.rowcount, "record(s) inserted.")


def get_first_laptop():
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {MYSQL_TABLE_NAME} LIMIT 1')
    result = cursor.fetchall()
    return result


def read_from_csv(csvfile) -> list[dict]:
    with open(csvfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        laptops = []
        for row in reader:
            laptops.append(row)
        return laptops


def main():
    clear_db()
    laptops = read_from_csv('dataset/laptops.csv')
    for laptop in laptops:
        if laptop.get('company', None) is None:
            print(laptop)
    insert_into_db(laptops)
    print(get_first_laptop())


if __name__ == '__main__':
    main()
