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

    def start_round(self, player1, player2, p1bets, p2bets):
        self.player1 = player1
        self.player2 = player2
        self.p1bets = p1bets
        self.p2bets = p2bets

    def end_round(self, duration, winner):
        self.duration = duration
        self.winner = winner

    def save_round(self):
        # TODO: Save to SQL
        return

def record_match(session, request):
    # Initialize a match
    site = website(session, request)

    while(True):
        # Add a delay to avoid overloading the server
        time.sleep(10)

        # Update status
        prev_status = site.get_betting_status()
        prev_balance = site.get_balance()
        site.update()
        status = site.get_betting_status()
        balance = site.get_balance()

        if (prev_status == 'locked' and status == 'open'):
            if (balance > prev_balance):
                print('Our bet wins')
            elif (balance < prev_balance):
                print('Our bet loses')
            else:
                print('Money remained the same')
                print(site.get_json())

            print('\nBetting is now open!')
            print('Balance: ' + str(balance))

            # Place the bet
            bet_player1(session, 500)

        elif (prev_status == 'open' and status == 'locked'):
            print('The match begins!')

