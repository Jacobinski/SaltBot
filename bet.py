'''
The betting module for SaltBot
'''
import json
import random
from enum import Enum

URL_BET = 'http://www.saltybet.com/ajax_place_bet.php'

class player(Enum):
    P1 = 'player1'
    P2 = 'player2'

def bet(session, player, wager):
    """
    Place a bet on a player

    Given an input player1 or player2, along with a wager, this function formats and sends SaltyBet a request for a bet.

    Args:
        session (session): A requests library session for the SaltyBet
            website.
        player (player): Either enum P1 or P2
        wager (int): The amount of money to wager.

    Returns:
        None

    """

    bet = {'selectedplayer': player.value, 'wager': wager}
    r = session.post(URL_BET, data=bet)

    assert r.status_code == 200, "Bet failed to be place. Code: %i" \
        % r.status_code

def determine_wager(total_money):
    """
    Determine a wager when given total money

    When placing bets, one should be careful to bet low amounts to not
    tip the betting pool too much in one direction. This being said, we
    should bet at a value high enough to make it worth our time.

    Args:
        total_money (int): The total money in our bank

    Returns:
        wager (int): The suggested wager to place

    """
    """
    First pass algorithm: Linear model
        Bet: $500,  Total: $100k
        Bet: $1000, Total: $200k

        Model:    y = m * x      + b
               1000 = m * 200000 + b
                500 = m * 100000 + b
                -> b = 0
                -> m = 0.005
    """

    return 500
    #return round(0.005 * total_money)
