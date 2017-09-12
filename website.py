'''
The match monitoring module for SaltBot
'''
from bs4 import BeautifulSoup
import requests
import time
import json

URL_JSON = "http://www.saltybet.com/state.json"

class website:
    def __init__(self, session, request):
        # Match session
        self.session = session
        self.request = request
        self.match_json = json.loads(session.get(URL_JSON).content)

        # Match Details
        soup = BeautifulSoup(request.content, 'html.parser')
        self.balance = int(soup.find(id="balance").string.replace(',',''))

    def update(self):
        # Refresh the request
        self.request = self.session.get(self.request.url)

        # Check to see if the match status changed
        new_match = json.loads(self.session.get(URL_JSON).content)

        if (self.match_json != new_match):
            soup = BeautifulSoup(self.request.content, 'html.parser')
            self.match_json = new_match
            self.balance = int(soup.find(id="balance").string.replace(',',''))

    def get_betting_status(self):
        return self.match_json['status']

    def get_balance(self):
        return self.balance

    def get_json(self):
        return self.match_json
