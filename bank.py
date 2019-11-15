#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from random import randint, sample
from time import sleep
import math
from cqc.pythonLib import CQCConnection, qubit

# Default coin size
coin_size = 4
# Global coin container
coins = []
# Global qubit pair container
pairs = []

k_index = 9
P = []

def create_coin(k):
    print("First stage")
    with CQCConnection("Alice") as Bank:
        # For each i-th coin
        for i in range(k):
            # Create a new empty coin
            coins.append([None] * coin_size)
            # Create a new qubit container
            pairs.append([None] * 2)
            # Create its P register
            P.append(i)

            # Iterate over the newly created coin
            print("Creating the classical random number sequence")
            for j in range(coin_size):
                # Create random bit
                random_bit = randint(0,1)
                # Assign random bit to the coin container
                coins[i][j] = random_bit
            print(coins[i])

            print('Creating qubits')
            # Create qubits: |0>
            q1 = qubit(Bank)
            q2 = qubit(Bank)

            for index, q in enumerate([q1, q2]):
                offset = int(2 * index)
		#See section 2 of pdf. Run through gates based on classical input. 
                q.H()
                print('Qubit', index+1, 'via Hardamand')
            
            # Store the encoded qubits
            pairs[i] = [q1, q2]
            print('Finished quantum register:', i)
            
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
    print('Full register')
    print(register_c)
    t=3*(randint(1,math.floor(len(register_c)/3)))
    print('t=',t)
    m_s = []
    list_of_random_indexes = random.sample(register_c, t)
    print('Bank chosen list of t indexes')
    print(list_of_random_indexes)
    with CQCConnection("Alice") as Bank:
        # Send the list of indexes
        Bank.sendClassical("Bob", list_of_random_indexes)
        # Wait for receiver
        sleep(1)
        index_list = Bank.recvClassical()
        rlist = list(index_list)
        print('Holder, Bob, chosen list of 2t/3 indexes')
        print(rlist)
        ## Wait for receiver
        sleep(1)
        print('Full register again')
        print(register_c)
	#foreach index in Bob's list, generate m= 0 or 1. 
	#mark index as used.
        for c,i in enumerate(rlist):
            register_c.remove(i)
            m_s.append(random.randint(0,1))
        print('Remaining unused registers')
        print(register_c)
        print('m= 0 or 1 for each index chosen by Bob')
        print(m_s)
        Bank.sendClassical("Bob", m_s)

    #FLush memory
    #Bank.flush()


if __name__ == "__main__":
    create_coin(k_index)
    
    verify_coin(range(k_index))

    parse_coin()


