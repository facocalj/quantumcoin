#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
#from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit

P = []
# Global qubit pair container
pairs = []

def receive_coin(k=9):
    print("First stage: Receive quantum registers for coin")
    with CQCConnection("Bob") as Bob:
        # For each i-th coin
        for i in range(k):
            # Create a new qubit container
            pairs.append([None] * 2)

            # Receive P and the qubit pair
            value = Bob.recvClassical()[0]
            q1 = Bob.recvQubit()
            q2 = Bob.recvQubit()
            pairs[i] = [q1, q2]

            print(value)

        sleep(1)

def verify_coin(k=9):
    print("Verify Coin ID 1")
    with CQCConnection("Bob") as Bob:
        register_c = list(range(k))#note hardcoded.
        print('Full register')
        print(register_c)
        list_of_random_indexes = list(Bob.recvClassical())
        print('Bank chosen list of t indexes')
        print(list_of_random_indexes)
        size = len(list_of_random_indexes)
        smaller_t=int(2*size/3)
        print('2t/3 = ',smaller_t)
        local_selection = random.sample(list_of_random_indexes, smaller_t)
        print('Holder, Bob, chosen list of 2t/3 indexes')
        print(local_selection)
        Bob.sendClassical("Alice", local_selection)
        print('Remaining unused registers')
        for c,i in enumerate(local_selection):
            register_c.remove(i)

        print(register_c)
        # Wait for receiver
        #sleep(1)
        m_s = Bob.recvClassical()
        print('Recieve m= 0 or 1 for each 2t/3 index chosen')
        print(list(m_s))

        for i in range(len(local_selection)):
            print("Index value", local_selection[i], ", M Value", m_s[i])


    # FLush memory
    #Bob.flush()


def send_coins():
    pass

if __name__ == "__main__":
    receive_coin()

    verify_coin()

    send_coins()

