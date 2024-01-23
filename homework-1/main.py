"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
from pathlib import Path

import psycopg2


def reform_to_list(file_path: Path) -> list[tuple]:
    """Возвращает список с кортежами значений из файла"""
    with open(file_path) as f:
        data_from_csv = csv.DictReader(f)
        data: dict
        file_list = []
        for data in data_from_csv:
            data_list = []
            for value in data.values():
                data_list.append(value)
            if len(data_list) == 6:
                data_tuple = (int(data_list[0]), data_list[1], data_list[2], data_list[3], data_list[4], data_list[5])
            elif len(data_list) == 5:
                data_tuple = (int(data_list[0]), data_list[1], int(data_list[2]), data_list[3], data_list[4])
            elif len(data_list) == 3:
                data_tuple = (data_list[0], data_list[1], data_list[2])
            file_list.append(data_tuple)
        return file_list


# Формируем пути к файлам
parents_path = Path(__file__).parent
file_path_customers = Path(parents_path, 'north_data', 'customers_data.csv')
file_path_employees = Path(parents_path, 'north_data', 'employees_data.csv')
file_path_orders = Path(parents_path, 'north_data', 'orders_data.csv')

# Устанавливаем связь с БД
conn = psycopg2.connect(
    host="localhost",
    database="north",
    user="postgres",
    password="12345"
)

try:
    with conn:
        with conn.cursor() as cur:
            # Заполняем таблицу 'customers'
            customers_data = reform_to_list(file_path_customers)
            for customer in customers_data:
                cur.execute("INSERT INTO customers VALUES (%s, %s, %s)", customer)

            # Заполняем таблицу 'employees'
            employees_data = reform_to_list(file_path_employees)
            for employee in employees_data:
                cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)", employee)

            # Заполняем таблицу 'orders'
            orders_data = reform_to_list(file_path_orders)
            for order in orders_data:
                cur.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)", order)
finally:
    conn.close()
