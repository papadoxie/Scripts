#!/usr/bin/env python

from boofuzz import Session, Target, TCPSocketConnection, fuzz_logger_text
from pwn import process
import asyncio

async def fuzz(session):
    await session.fuzz()

def main():

    try:
        session = Session(
            target = Target(connection = TCPSocketConnection('127.0.0.1', 4444))
            # process('example.exe')
           )
        print('Session Started')

    except:
        print('Failed to start session')

    try:
        fuzz(session)
        print('Fuzzing')
    except:
        print('Fuzzing Failed')

if __name__ == '__main__':
    main()