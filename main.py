'''
A python script for SaltBot
'''
import os
import sys
import time
from enum import Enum

import requests
from urllib import parse
from bs4 import BeautifulSoup
import psycopg2

from login import saltbot_login
from match import record_match
from bet import bet, player, determine_wager
from website import website


parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["SALTBOT_DATABASE_URL"])

class match_state(Enum):
    p1_win = 0
    p2_win = 1
    tie = 3
    invalid = 4

def main():
    """
    The main run loop for SaltBot

    """
    # Login to SaltyBet
    session, request = saltbot_login()

    # Connect to Database
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()

    # Record the match
    site = website(session, request)
    balance_start, balance_end = site.get_balance(), site.get_balance()
    status, prev_status = "None", "None"
    duration = 0
    placed_bet = False
    state = match_state.invalid

    # Create a match dictionary
    match = {'player1':'','player2':'','duration':'', 'p1bet':'',
    'p2bet':'', 'myplayer':'', 'mybet':'', 'winner':''}

    while(True):
        try:
            # Add a delay to avoid overloading the server
            time.sleep(10)
            duration += 10

            # Update status
            prev_status = status
            site.update()
            status = site.get_betting_status()

            # Note: The status can be open, locked, 1, 2. The last two
            # statuses denote player1, player2 victory
            if (prev_status != 'open' and status == 'open'):
                # End of previous match.
                # The placed_bet check is these to ensure that the match had begun and we fully populated the match dict before storing to PostgreSQL
                if placed_bet:

                    balance_end = site.get_balance()

                    if (balance_end > balance_start):
                        print('Our bet wins')
                        match['winner'] = match['myplayer']
                        if match['player1'] == match['myplayer']:
                            state = match_state.p1_win
                        else:
                            state = match_state.p2_win
                    elif (balance_end < balance_start):
                        print('Our bet loses')
                        if match['myplayer'] == match['player1']:
                            match['winner'] = match['player2']
                            state = match_state.p2_win
                        else:
                            match['winner'] = match['player1']
                            state = match_state.p1_win
                    else:
                        print('Start $: ' + str(balance_start)
                            + ' End $: ' + str(balance_end))
                        print('Money remained the same?')
                        match['winner'] = '???'
                        state = match_state.tie

                    match['duration'] = duration

                    # Save the match
                    cur.execute(""" INSERT INTO Match (player1, player2,
                        duration_s, p1_bets, p2_bets, my_player, my_bet,
                        winner) VALUES (%s, %s, %s, %s, %s, %s,
                        %s, %s)""", (match['player1'], match['player2'],
                        match['duration'], match['p1bet'],
                        match['p2bet'], match['myplayer'],
                        match['mybet'], match['winner']))
                    conn.commit()

                # Start of new match
                print('\nBetting is now open!')
                print('Balance: ' + str(balance_end))

                wager = determine_wager(balance_end)

                # Place the bet, refresh the status to determine success
                bet(session, player.P1, wager)
                placed_bet = True
                print("Bet " + str(wager) + " on " + player.P1.value)
                match['myplayer'] = site.get_player1_name()
                match['mybet'] = wager

            elif (prev_status == 'open' and status == 'locked'):
                print('The match begins!')
                balance_start = site.get_balance()
                duration = 0

                match['player1'] = site.get_player1_name()
                match['player2'] = site.get_player2_name()
                match['p1bet'] = site.get_player1_wagers()
                match['p2bet'] = site.get_player2_wagers()

        except Exception as err:
            cur.close()
            conn.close()
            sys.stderr.write('ERROR: %s \n' % str(err))

if __name__ == '__main__':
    main()