'''
A python script for SaltBot
'''
import sys
import requests
import time
from bs4 import BeautifulSoup

from login import saltbot_login
from match import record_match
from bet import bet_player1
from website import website

# New
import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])


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
    balance_start, balance_end = None, None
    status, prev_status = None, None

    while(True):
        try:
            # Add a delay to avoid overloading the server
            time.sleep(10)

            # Update status
            prev_status = status
            site.update()
            status = site.get_betting_status()

            if (prev_status == 'locked' and status == 'open'):
                balance_end = site.get_balance()
                if (balance_end > balance_start):
                    print('Our bet wins')
                elif (balance_end < balance_start):
                    print('Our bet loses')
                else:
                    print('Start $: ' + str(balance_start)
                        + ' End $: ' + str(balance_end))
                    print('Money remained the same?')
                print(site.get_json())

                print('\nBetting is now open!')
                print('Balance: ' + str(balance_end))

                # Place the bet
                bet_player1(session, 500)

            elif (prev_status == 'open' and status == 'locked'):
                print('The match begins!')
                balance_start = site.get_balance()

                cur.execute(""" INSERT INTO Match (player1, player2,
                    duration_s, p1_bets, p2_bets, my_player, my_bet, winner,
                    tier) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (site.get_player1_name(), site.get_player2_name(), 0,
                    site.get_player1_wagers(),site.get_player2_wagers(),
                    site.get_player1_name(), 500, "TODO: Fix unknown winner",
                    "?"))
                conn.commit()

        except Exception, err:
            cur.close()
            conn.close()
            sys.stderr.write('ERROR: %sn' % str(err))

if __name__ == '__main__':
    main()