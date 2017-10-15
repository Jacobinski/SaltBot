# SaltBot
[![Build Status](https://travis-ci.org/Jacobinski/SaltBot.svg?branch=master)](https://travis-ci.org/Jacobinski/SaltBot)

An automatic betting program for www.saltybet.com

## Usage
### Authentication
The user's email and password must be set as environment variables in order for Saltbot to use the account. This can be done from command line.
```bash
$ export SALTBOT_EMAIL = "example@example.com"
$ export SALTBOT_PASSWORD = "examplePassword123"
```
### Database Setup
Saltbot currently only supports Heroku Postgresql databases. These can be obtained through **data.heroku.com**, and the provided DATABASE_URL from Heroku serves as the environment variable.
```bash
$ export SALTBOT_DATABASE_URL = "postgres://USER:PASSWORD@HOST:PORT/DATABASE
```
### Python Setup
This bot is programmed in Python 3.6, so it must be installed on your machine. Check to make sure it is installed.
```bash
$ python --version
Python 3.6.0
```
Use pip3 to install the requirements.txt
```bash
$ pip3 install -r requirements.txt
```
### Running the Bot
The current state of the bot is to place $500 on Red each round. To run the command, invoke the following command from the console.
```bash
$ python3 main.py
```
