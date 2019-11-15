#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
#from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit

# Default coin size
coin_size = 4
# Global coin container
coins = []
# Global qubit pair container
pairs = []

k_index = 8
P = []

def create_coin(k):
    print("First stage")
    with CQCConnection("Alice") as Bank:
        # For each i-th coin
        for i in range(k):
            print("Creating the random number sequence")
            # Create a new empty coin
            coins.append([None] * coin_size)
            # Create a new qubit container
            pairs.append([None] * 2)
            # Create its P register
            P.append(i)

            # Iterate over the newly created coin
            for j in range(coin_size):
                # Create random bit
                random_bit = 0
                # Assign random bit to the coin container
                coins[i][j] = random_bit

            print(coins[i])

            print('Creating qubits')
            # Create qubits: |0>
            q1 = qubit(Bank)
            q2 = qubit(Bank)

            for index, q in enumerate([q1, q2]):
                offset = int(2 * index)

                q.H()
                print('Qubit', index+1, 'via Hardamand')
            
            # Store the encoded qubits
            pairs[i] = [q1, q2]
            print('Finished coin:', i)
            
            # Send the identifier
            Bank.sendClassical("Bob", P[i])
            # Send first half of the two qubits
            Bank.sendQubit(pairs[i][0], "Bob")
            # Send second half of the two particles
            Bank.sendQubit(pairs[i][1], "Bob")

            print('Sent Coin #', P[i])
            # Wait for receiver
            sleep(1)
        # FLush memory
        Bank.flush()

def parse_coin():
    pass

def verify_coin(register):
    # Hardcoding t at this point - to be randomised later
    register_c = list(register)
    print(register_c)
    t=3
    m_s = []
    list_of_random_indexes = random.sample(register_c, t)
    print(list_of_random_indexes)
    with CQCConnection("Alice") as Bank:
        # Send the list or indexes
        Bank.sendClassical("Bob", list_of_random_indexes)
        # Wait for receiver
        #sleep(1)
        index_list = Bank.recvClassical()
        rlist = list(index_list)
        print(rlist)
        ## Wait for receiver
        sleep(1)
        print(register_c)
        for c,i in enumerate(rlist):
            register_c.remove(i)
            m_s.append(random.randint(0,1))

        print(register_c)
        print(m_s)
        Bank.sendClassical("Bob", m_s)

    # FLush memory
    #Bank.flush()


if __name__ == "__main__":
    #create_coin(k_index)
    
    verify_coin(range(k_index))

    parse_coin()

