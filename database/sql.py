import psycopg2

def record_win(name, duration, conn, cur):
    cur.execute(
        "update player"
        "set matches = matches + 1,"
        "    win_percentage = (1.0 * wins + 1) / (wins + losses + 1),"
        "    wins = wins + 1,"
        "    avg_win_time = (1.0 * wins * avg_win_time + %s ) / (wins + 1) "
        "where name = %s",
        (duration, name))
    conn.commit()

def record_loss(name, duration, conn, cur):
    cur.execute(
        "update player"
        "set matches = matches + 1,"
        "    win_percentage = (1.0 * wins) / (wins + losses + 1),"
        "    losses = losses + 1,"
        "    avg_lose_time = (1.0 * losses * avg_lose_time + %s ) / (losses + 1) "
        "where name = %s",
        (duration, name))
    conn.commit()

def record_tie(name1, name2, conn, cur)
    cur.execute(
        "update player"
        "set matches = matches + 1,"
        "    ties = ties + 1 "
        "where name = %s or name = %s",
        (name1, name2))
    conn.commit()