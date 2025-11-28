from mysql.connector import MySQLConnection, Error
from mysql.connector.cursor import MySQLCursor
import mysql.connector
import os
config = {
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_DATABASE'),
}


def only_execute_query(query, params):
    print("IN extecute query")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        print("OUT extecute query")
        row = cursor.fetchone()
        return row
    finally:
        cursor.close()
        conn.close()


def execute_query(query, params):
    print("IN extecute query")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        print("OUT extecute query")
        return cursor.lastrowid
    except mysql.connector.IntegrityError as e:
        print("Error inserting record: ", e)
        print("Record already exists")
    finally:
        cursor.close()
        conn.close()


def find_match(query, show=False):
    print("IN find match")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        a = cursor.fetchall()
        if show != True:
            conn.commit()
        print("OUT find match")
        if show == True:
            titles = [description[0] for description in cursor.description]
            print(titles)
        return a
    finally:
        cursor.close()
        conn.close()


# def main():
#     queryRunner(query)


if __name__ == '__main__':
    main()
