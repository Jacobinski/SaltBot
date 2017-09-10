'''
The betting module for SaltBot
'''
import json
import random

URL_BET = 'http://www.saltybet.com/ajax_place_bet.php'

def __bet(session, player, wager):
    bet = {'selectedplayer': player, 'wager': wager}
    session.post(URL_BET, data=bet)
    if ('player1' == player):
        print("Wager " + bet['wager'] + " on " + json.loads(session.get("http://www.saltybet.com/state.json").content)['p1name'])
    elif('player2' == player):
        print("Wager " + bet['wager'] + " on " + json.loads(session.get("http://www.saltybet.com/state.json").content)['p2name'])

def bet_player1(session, wager):
    __bet(session, 'player1', str(wager))

def bet_player2(session, wager):
    __bet(session, 'player2', str(wager))

def bet_random(session, wager):
    player = random.randint(1,2)
    if (1 == player):
        __bet(session, 'player1', str(wager))
    elif (2 == player):
        __bet(session, 'player2', str(wager))
    else:
        print("Bet random failed")