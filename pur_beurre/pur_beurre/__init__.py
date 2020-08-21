import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

if os.environ.get('IS_HEROKU', None):
    DATABASE = os.environ['DATABASE_URL']
else:
    DATABASE = "dbname=postgres"


def create_db():
    sql = "CREATE DATABASE pur_beurre WITH ENCODING='utf8'"
    try:
        conn = psycopg2.connect(DATABASE)
        print("1")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print("2")
        c = conn.cursor()
        print("3")
        c.execute(sql)
        print("4")
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False


def exist_db():
    exist = True
    try:
        conn = psycopg2.connect(DATABASE)
        conn.close()
    except psycopg2.OperationalError as e:
        exist = False
    return exist


if not exist_db() and not os.environ.get('IS_HEROKU', False):
    print("[!] No DB")
    if create_db():
        print("[*] DB created")
    else:
        print("[*] Error")
