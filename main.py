'''
A python script for SaltBot
'''
from bs4 import BeautifulSoup
import requests
import time
import json

from login import saltbot_login

URL_BET = 'http://www.saltybet.com/ajax_place_bet.php'

def main():
    # Login to SaltyBet
    session, request = saltbot_login()

    while(True):
        # Add a delay to avoid overloading the server
        time.sleep(40)

        # Refresh and get the balance
        request = session.get(request.url)
        soup = BeautifulSoup(request.content, 'html.parser')
        balance = int(soup.find(id="balance").string.replace(',',''))
        print("balance: " + str(balance))

        # Determine the state of the match
        if(json.loads(session.get("http://www.saltybet.com/state.json").content)['status'] == 'open'):
            # Place the bet
            red_bet = {'selectedplayer': 'player1', 'wager': '500'}
            session.post(URL_BET, data=red_bet)
            print("Wager " + red_bet['wager'] + " on " + json.loads(session.get("http://www.saltybet.com/state.json").content)['p1name'])

if __name__ == '__main__':
    main()