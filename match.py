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

def get_balance(session, request):
    soup = BeautifulSoup(request.content, 'html.parser')
    balance = int(soup.find(id="balance").string.replace(',',''))
    return balance

class Match:
    def __init__(self, session, request):
        self.session = session
        self.request = request
        self.match_json = json.loads(session.get(URL_JSON).content)
        self.status = self.match_json['status']
        self.balance = get_balance(session, request)

    def update_match(self):
        # Refresh the request
        self.request = self.session.get(self.request.url)

        # Check to see if the match status changed
        new_match = json.loads(self.session.get(URL_JSON).content)
        if (self.match_json != new_match):
            self.match_json = new_match
            self.status = self.match_json['status']

    def get_status(self):
        return self.status


def record_match(session, request):
    # Initialize a match
    match = Match(session, request)

    while(True):
        # Add a delay to avoid overloading the server
        time.sleep(10)

        # Update match status
        match.update_match()

        # Print balance
        print('Balance: ' + str(get_balance(session, request)))

        # Determine the state of the match
        if(match.get_status() == 'open'):
            # Place the bet
            bet_player1(session, 500)
