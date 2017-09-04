'''
The user login module for SaltBot
'''
import requests
import yaml

URL_SIGNIN = 'https://www.saltybet.com/authenticate?signin=1'

def saltbot_login():
    # Default the return values to None
    session = None
    request = None

    with open("login.yaml", 'r') as credentials:
        try:
            # Start a session so we can have persistant cookies
            session = requests.session()

            # Obtain login specifics from login.yaml
            login_yaml = yaml.load(credentials)

            # This is the form data that the page sends when logging in
            login_data = {
                'email': login_yaml['email'],
                'pword': login_yaml['password'],
                'authenticate': 'signin'
            }

            # Authenticate
            request = session.post(URL_SIGNIN, data=login_data)

            # Check for successful login & redirect
            if request.url != "https://www.saltybet.com/" and request.url != "http://www.saltybet.com/":
                print("Error: Wrong URL: " + request.url)

        except yaml.YAMLError as exc:
            print(exc)

        return session, request