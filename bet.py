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

    bet = {'selectedplayer': player, 'wager': wager}
    r = session.post(URL_BET, data=bet)

    assert r.status_code == 200, "Bet failed to be place. Code: %i" \
        % r.status_code