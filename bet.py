'''
The betting module for SaltBot
'''
import json
import random

URL_BET = 'http://www.saltybet.com/ajax_place_bet.php'

def __bet(session, player, wager):
    """
    Place a bet on a player

    Given an input player1 or player2, along with a wager, this function formats and sends SaltyBet a request for a bet.

    Args:
        session (session): A requests library session for the SaltyBet
            website.
        player (str): Either "player1" or "player2".
        wager (int): The amount of money to wager.

    Returns:
        None

    """

    bet = {'selectedplayer': player, 'wager': wager}
    session.post(URL_BET, data=bet)

    if ('player1' == player):
        print("Wager " + bet['wager'] + " on " + json.loads(session.get("http://www.saltybet.com/state.json").content)['p1name'])
    elif('player2' == player):
        print("Wager " + bet['wager'] + " on " + json.loads(session.get("http://www.saltybet.com/state.json").content)['p2name'])

def bet_player1(session, wager):
    """
    Place a bet on a player1

    Given a wager, this function formats and sends SaltyBet a request for
    a bet.

    Args:
        session (session): A requests library session for the SaltyBet
            website.
        wager (int): The amount of money to wager.

    Returns:
        None

    """

    __bet(session, 'player1', str(wager))

def bet_player2(session, wager):
    """
    Place a bet on a player2

    Given a wager, this function formats and sends SaltyBet a request for
    a bet.

    Args:
        session (session): A requests library session for the SaltyBet
            website.
        wager (int): The amount of money to wager.

    Returns:
        None

    """

    __bet(session, 'player2', str(wager))

def bet_random(session, wager):
    """
    Place a bet on a random player

    Given a wager, this function formats and sends SaltyBet a request for
    a bet.

    Args:
        session (session): A requests library session for the SaltyBet
            website.
        wager (int): The amount of money to wager.

    Returns:
        None

    """

    player = random.randint(1,2)
    if (1 == player):
        __bet(session, 'player1', str(wager))
    elif (2 == player):
        __bet(session, 'player2', str(wager))
    else:
        print("Bet random failed")