'''
The match monitoring module for SaltBot
'''
from bs4 import BeautifulSoup
import requests
import time
import json

from login import saltbot_login
from bet import bet_player1

URL_JSON = "http://www.saltybet.com/state.json"

class Match:
    def __init__(self, session, request):
        soup = BeautifulSoup(request.content, 'html.parser')
        self.session = session
        self.request = request
        self.match_json = json.loads(session.get(URL_JSON).content)
        self.betting_status = self.match_json['status']
        self.balance = int(soup.find(id="balance").string.replace(',',''))

    def update(self):
        # Refresh the request
        self.request = self.session.get(self.request.url)

        # Check to see if the match status changed
        new_match = json.loads(self.session.get(URL_JSON).content)
        if (self.match_json != new_match):
            # Update match json
            self.match_json = new_match

            # Update betting status
            self.betting_status = self.match_json['status']

            # Update balance
            soup = BeautifulSoup(self.request.content, 'html.parser')
            self.balance = int(soup.find(id="balance").string.replace(',',''))

    def get_betting_status(self):
        return self.betting_status

    def get_balance(self):
        return self.balance


def record_match(session, request):
    # Initialize a match
    match = Match(session, request)

    while(True):
        # Add a delay to avoid overloading the server
        time.sleep(10)

        # Update match status
        prev_status = match.get_betting_status()
        prev_balance = match.get_balance()
        match.update()
        status = match.get_betting_status()
        balance = match.get_balance()

        if (prev_status == 'locked' and status == 'open'):
            if (balance > prev_balance):
                print('Our bet wins')
            elif (balance < prev_balance):
                print('Our bet loses')
            else:
                print('Money remained the same')

            print('\nBetting is now open!')
            print('Balance: ' + str(balance))

            # Place the bet
            bet_player1(session, 500)

        elif (prev_status == 'open' and status == 'locked'):
            print('The match begins!')

