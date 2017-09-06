'''
A python script for SaltBot
'''
from bs4 import BeautifulSoup
import requests
import time
import json

from login import saltbot_login
from bet import bet_player1

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
            bet_player1(session, 100)

if __name__ == '__main__':
    main()