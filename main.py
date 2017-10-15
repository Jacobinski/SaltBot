'''
A python script for SaltBot
'''
import os
import sys
import time

import requests
from urllib import parse
from bs4 import BeautifulSoup
import psycopg2

from match import record_match
from bet import bet, player, determine_wager
from state_machine import match_state
import website
import database
import authenticate

def main():
    """
    The main run loop for SaltBot

    """

    # Login to SaltyBet
    session, request = authenticate.login()

    # Connect to Database
    conn, cur = database.connect()

    # Setup website interface
    site = website.interface(session, request)

    # Create global variables
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
                    database.save_match(match, conn, cur)

                    # Add players to table if not already there
                    for p in [match['player1'],match['player2']]:
                        if not database.has_player(p, cur):
                            database.add_player(p, conn, cur)

                    # Update player tables
                    if match_state.p1_win == state:
                        database.record_win(match['player1'], match['duration'], conn, cur)
                        database.record_loss(match['player2'], match['duration'], conn, cur)
                    elif match_state.p2_win == state:
                        database.record_win(match['player2'], match['duration'], conn, cur)
                        database.record_loss(match['player1'], match['duration'], conn, cur)
                    elif match_state.tie == state:
                        database.record_tie(match['player1'], match['player2'], conn, cur)

                # Start of new match
                print('\nBetting is now open!')
                print('Balance: ' + str(balance_end))

                wager = determine_wager(balance_end)

                # Place the bet, refresh the status to determine success
                bet(session, player.P1, wager)
                placed_bet = True
                print("Bet " + str(wager) + " on " + match['player1'])

                match['player1'] = site.get_player1_name()
                match['player2'] = site.get_player2_name()
                match['myplayer'] = site.get_player1_name()
                match['mybet'] = wager
                #print(database.get_player(match['player1'], cur))
                #print(database.get_player(match['player2'], cur))

            elif (prev_status == 'open' and status == 'locked'):
                print('The match begins!')
                balance_start = site.get_balance()
                duration = 0

                match['p1bet'] = site.get_player1_wagers()
                match['p2bet'] = site.get_player2_wagers()

        except Exception as err:
            cur.close()
            conn.close()
            sys.stderr.write('ERROR: {0} on line {1}\n'.format(
                str(err), sys.exc_info()[-1].tb_lineno))

if __name__ == '__main__':
    main()