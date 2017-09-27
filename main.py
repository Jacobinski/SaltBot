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

def main():
    """
    The main run loop for SaltBot

    """

    # Login to SaltyBet
    session, request = saltbot_login()

    # Record the match
    site = website(session, request)
    balance_start, balance_end = None, None

    while(True):
        try:
            # Add a delay to avoid overloading the server
            time.sleep(10)

            # Update status
            prev_status = site.get_betting_status()
            site.update()
            status = site.get_betting_status()

            if (prev_status == 'locked' and status == 'open'):
                balance_end = site.get_balance()
                if (balance_end > balance_start):
                    print('Our bet wins')
                elif (balance_end < balance_start):
                    print('Our bet loses')
                else:
                    print('Money remained the same')
                    print(site.get_json())

                print('\nBetting is now open!')
                print('Balance: ' + str(balance_end))

                # Place the bet
                bet_player1(session, 500)

            elif (prev_status == 'open' and status == 'locked'):
                print('The match begins!')
                balance_start = site.get_balance()

        except Exception, err:
            sys.stderr.write('ERROR: %sn' % str(err))

if __name__ == '__main__':
    main()