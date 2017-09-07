'''
The user login module for SaltBot
'''
import requests
import os
from dotenv import load_dotenv, find_dotenv

URL_SIGNIN = 'https://www.saltybet.com/authenticate?signin=1'

def saltbot_login():
    # Default the return values to None
    session = None
    request = None

    # Start a session so we can have persistant cookies
    session = requests.session()

    # Obtain login specifics from .env
    load_dotenv(find_dotenv())

    # This is the form data that the page sends when logging in
    login_data = {
        'email': os.environ.get('EMAIL'),
        'pword': os.environ.get('PASSWORD'),
        'authenticate': 'signin'
    }

    # Authenticate
    request = session.post(URL_SIGNIN, data=login_data)

    # Check for successful login & redirect
    if request.url != "https://www.saltybet.com/" and request.url != "http://www.saltybet.com/":
        print("Error: Wrong URL: " + request.url)

    return session, request