import os
import psycopg2
import urlparse

def connect():
    urlparse.uses_netloc.append("postgres")
    URL = urlparse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=URL.path[1:],
        user=URL.username,
        password=URL.password,
        host=URL.hostname,
        port=URL.port
    )
    cur = conn.cursor()

    return conn, cur