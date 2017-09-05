# SaltBot
[![Build Status](https://travis-ci.org/Jacobinski/SaltBot.svg?branch=master)](https://travis-ci.org/Jacobinski/SaltBot)

An automatic betting program for www.saltybet.com

## Usage
### Authentication
Create a file named **login.yaml** in the same directory as login.py. Add your SaltyBet account's username and password to it.
```YAML
# This is an example login.yaml
email: someone@example.com
password: examplepassword
```
### Python Setup
This bot is programmed in Python 2.7, so it must be installed on your machine. Check to make sure it is installed.
```bash
$ python --version
Python 2.7.13
```
Use pip to install the requirements.txt
```bash
$ pip install -r requirements.txt
```
### Running the Bot
The current state of the bot is to place $500 on Red each round. To run the command, invoke the following command from the console.
```bash
$ python main.py
```
