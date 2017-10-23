import psycopg2

def record_win(name, duration, conn, cur):
    """
    Record a player win in the database

    Update the player SQL object to reflect that they just won.

    Args:
        name (str): The name of the player
        duration (int): The duration of the match, in seconds
        conn: The SQL connection object
        cur: The SQL cursor

    Returns:
        None

    """
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
    """
    Record a player loss in the database

    Update the player SQL object to reflect that they just lost.

    Args:
        name (str): The name of the player
        duration (int): The duration of the match, in seconds
        conn: The SQL connection object
        cur: The SQL cursor

    Returns:
        None

    """
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
    """
    Record a set of ties in the database

    Update both player's SQL object to reflect that they tied.

    Args:
        name1 (str): The name of a player
        name2 (str): The name of a different player
        conn: The SQL connection object
        cur: The SQL cursor

    Returns:
        None

    """
    cur.execute(
        "update player "
        "set matches = matches + 1,"
        "    ties = ties + 1 "
        "where name = %s or name = %s",
        (name1, name2))
    conn.commit()

def save_match(match, conn, cur):
    """
    Save a match to the database

    Save the statistics of a match into the database.

    Args:
        match (dict): A dictionary holding match information
        conn: The SQL connection object
        cur: The SQL cursor

    Returns:
        None

    """
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
    """
    Determine if database has a player

    Returns a boolean indicating if the given player is in the database.

    Args:
        name (str): The player's name
        cur: The SQL cursor

    Returns:
        True if player is in database, else False

    """
    cur.execute(
        "select True "
        "from player "
        "where name = (%s)",
        (name,))
    if cur.fetchone() == None:
        return False
    else:
        return True

def add_player(name, conn, cur):
    """
    Save a player to the database

    Args:
        match (dict): A dictionary holding match information
        conn: The SQL connection object
        cur: The SQL cursor

    Returns:
        None

    """
    cur.execute(
        "insert into player "
        "    ( "
        "    name, matches, wins, losses, ties, "
        "    win_percentage, avg_win_time, avg_lose_time "
        "    ) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s)",
        (name, 0, 0, 0, 0, 0, 0, 0))
    conn.commit()

def get_player(name, cur):
    """
    Gets a player from the database

    Gets FIRST player with a given name's row from the database. This
    includes name, matches, wins, losses, ties, win percentage, average
    win time, average lose time. If two rows with the same name are
    present, one will be returned.

    Args:
        name (str): The player's name
        cur: The SQL cursor

    Returns:
        player (list): A list of the player features in the order: [name,
        matches, wins, losses, ties, win percentage, average win time,
        average lose time]

    """
    cur.execute(
        "select * "
        "from player "
        "where name = (%s)",
        (name,))
    ret = cur.fetchone()
    if ret == None:
        ret = ""
    return ret

def get_player_percent_wins(name, cur):
    """
    Gets a player's percent wins from the database

    Gets FIRST player with a given name's percent wins from the database.
    If two players with the same name are present, only one will be returned.

    Args:
        name (str): The player's name
        cur: The SQL cursor

    Returns:
        percent wins (float): A win percentage of the given player

    """
    if has_player(name, cur):
        return get_player(name, cur)[6]
    else:
        return None