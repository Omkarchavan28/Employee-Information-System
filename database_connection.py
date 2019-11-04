from sqlite3 import Error
import sqlite3
from sqlite3 import IntegrityError


# functions
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def create_table(conn,create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print("error is",e)


def create_project(conn,project,sql):
    cur = conn.cursor()
    cur.execute(sql,project)
    return cur.lastrowid
