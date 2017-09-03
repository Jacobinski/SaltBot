"""
A python script for SaltBot
"""
from bs4 import BeautifulSoup
import requests
import yaml
import time
import json

URL_SIGNIN = 'https://www.saltybet.com/authenticate?signin=1'
URL_BET = 'http://www.saltybet.com/ajax_place_bet.php'

def main():
    with open("login.yaml", 'r') as stream:
        try:
            # Start a session so we can have persistant cookies
            session = requests.session()

            # Obtain login specifics from login.yaml
            login_yaml = yaml.load(stream)

            # This is the form data that the page sends when logging in
            login_data = {
                'email': login_yaml['email'],
                'pword': login_yaml['password'],
                'authenticate': 'signin'
            }

            # Authenticate
            r = session.post(URL_SIGNIN, data=login_data)

            # Check for successful login & redirect
            if r.url != "https://www.saltybet.com/" and r.url != "http://www.saltybet.com/":
                print("Error: Wrong URL: " + r.url)
                return

            while(True):
                # Add a delay to avoid overloading the server
                time.sleep(40)

                # Refresh and get the balance
                r = session.get(r.url)
                soup = BeautifulSoup(r.content, 'html.parser')
                balance = int(soup.find(id="balance").string.replace(',',''))
                print("balance: " + str(balance))

                # Determine the state of the match
                if(json.loads(session.get("http://www.saltybet.com/state.json").content)['status'] == 'open'):
                    # Place the bet
                    red_bet = {'selectedplayer': 'player1', 'wager': '500'}
                    session.post(URL_BET, data=red_bet)
                    print("Wager " + red_bet['wager'] + " on " + json.loads(session.get("http://www.saltybet.com/state.json").content)['p1name'])

        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    main()