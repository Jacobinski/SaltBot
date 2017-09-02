"""
A python script for SaltBot

Inspiration from:
http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/
http://kazuar.github.io/scraping-tutorial/
"""
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
            print(r.url)

        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    main()