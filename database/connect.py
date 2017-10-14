import os

import psycopg2
from urllib import parse

def connect():
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["SALTBOT_DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()

    return conn, cur