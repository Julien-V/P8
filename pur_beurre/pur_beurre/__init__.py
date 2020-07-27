import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_db():
    sql = "CREATE DATABASE pur_beurre WITH ENCODING='utf8'"
    try:
        conn = psycopg2.connect("dbname=postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        c = conn.cursor()
        c.execute(sql)
        conn.close()
    except Exception as e:
        print(e)


def exist_db():
    exist = True
    try:
        conn = psycopg2.connect('dbname=pur_beurre')
        conn.close()
    except psycopg2.OperationalError as e:
        exist = False
    return exist


if not exist_db():
    print("[!] No DB")
    create_db()
    print("[*] DB created")
