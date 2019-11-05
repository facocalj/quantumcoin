#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit

P = []
# Global qubit pair container
pairs = []

def receive_coin(k=2):
    print("First stage: Receive coins")
    with CQCConnection("Bob") as Bob:
        # For each i-th coin
        for i in range(k):
            # Create a new qubit container
            pairs.append([None] * 2)

            value = Bob.recvClassical()[0]
            q1 = Bob.recvQubit()
            q2 = Bob.recvQubit()
            pairs[i] = [q1, q2]

            print(value)

        sleep(1)
if __name__ == "__main__":
    receive_coin()
