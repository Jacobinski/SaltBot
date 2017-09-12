'''
The match monitoring module for SaltBot
'''
from bs4 import BeautifulSoup
import requests
import time

from bet import bet_player1
from website import website

class Match:
    def __init__(self):
        self.id = 0         # TODO: Use SQL to determine this w/ MAX()
        self.player1 = None
        self.player2 = None
        self.duration = None
        self.winner = None
        self.p1bets = None
        self.p2bets = None
        self.mybet = None

    def start_round(self, mybet, website):
        self.player1 = website.get_player1_name()
        self.player2 = website.get_player2_name()
        self.p1bets = website.get_player1_wagers()
        self.p2bets = website.get_player2_wagers()
        self.mybet = mybet

    def end_round(self, duration, winner):
        self.duration = duration
        self.winner = winner

    def save_round(self):
        # TODO: Save to SQL
        return

def record_match(session, request):
    # Initialize a match
    site = website(session, request)
    balance_start = None
    balance_end = None

    while(True):
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

