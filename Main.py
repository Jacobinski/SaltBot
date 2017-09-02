"""
A python script for SaltBot
"""
from bs4 import BeautifulSoup
import requests
import yaml

URL_SIGNIN = 'https://www.saltybet.com/authenticate?signin=1'

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

            # Scrape for values
            soup = BeautifulSoup(r.content, 'html.parser')
            balance = int(soup.find(id="balance").string.replace(',',''))r
            print(balance)

            '''
            Betting is
            selectedplayer:player1
            wager:1
            '''

        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    main()