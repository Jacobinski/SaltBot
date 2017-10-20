import psycopg2

def record_win(name, duration, conn, cur):
    cur.execute(
        "update player "
        "set matches = matches + 1,"
        "    win_percentage = (1.0 * wins + 1) / (wins + losses + 1),"
        "    wins = wins + 1,"
        "    avg_win_time = (1.0 * wins * avg_win_time + %s ) / (wins + 1) "
        "where name = %s",
        (duration, name))
    conn.commit()

def record_loss(name, duration, conn, cur):
    cur.execute(
        "update player "
        "set matches = matches + 1,"
        "    win_percentage = (1.0 * wins) / (wins + losses + 1),"
        "    losses = losses + 1,"
        "    avg_lose_time = (1.0 * losses * avg_lose_time + %s ) / (losses + 1) "
        "where name = %s",
        (duration, name))
    conn.commit()

def record_tie(name1, name2, conn, cur):
    cur.execute(
        "update player "
        "set matches = matches + 1,"
        "    ties = ties + 1 "
        "where name = %s or name = %s",
        (name1, name2))
    conn.commit()

def save_match(match, conn, cur):
    cur.execute(
        "insert into match "
        "    ( "
        "    player1, player2, duration_s, p1_bets, "
        "    p2_bets, my_player, my_bet, winner "
        "    ) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s)",
        (match['player1'], match['player2'], match['duration'], match['p1bet'],
        match['p2bet'], match['myplayer'], match['mybet'], match['winner']))
    conn.commit()

def has_player(name, cur):
    cur.execute(
        "select True "
        "from player "
        "where name = (%s)"
        (name,))
    if cur.fetchone() == None:
        return False
    else:
        return True

def add_player(name, conn, cur):
    cur.execute(
        "insert into player "
        "    ( "
        "    name, matches, wins, losses, ties, "
        "    win_percentage, avg_win_time, avg_lose_time "
        "    ) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s)",
        (name, 0, 0, 0, 0, 0, 0, 0))
    conn.commit()