#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit

# Default coin size
coin_size = 4
# Global coin container
coins = []
# Global qubit pair container
pairs = []

P = []

def create_coin(k=2):
    print("First stage")
    with CQCConnection("Bank") as Bank:
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
                random_bit = randint(0,1)
                # Assign random bit to the coin container
                coins[i][j] = random_bit

            print(coins[i])

            print('Creating qubits')
            # Create qubits: |0>
            q1 = qubit(Bank)
            q2 = qubit(Bank)

            print('Modulating qubits:')
            # Encode coins into qubits
            for index, q in enumerate([q1, q2]):
                offset = int(2 * index)
                if coins[i][0+offset:2+offset] == [0,0]:
                    # |0>
                    print('Qubit', index+1, 'Encode: |0>' )

                elif coins[i][0+offset:2+offset] == [0,1]:
                    q.X()
                    print('Qubit', index+1, 'Encode: |1>')

                elif coins[i][0+offset:2+offset] == [1,0]:
                    # |1>
                    q.X()
                    # |0>-|1>/2
                    q.H()
                    print('Qubit', index+1, 'Encode: (|0>-|1>)/2')

                elif coins[i][0+offset:2+offset] == [1,1]:
                    # |0>+|1>/2
                    q.H()
                    print('Qubit', index+1, 'Encode: (|0>+|1>)/2')

                else:
                    print('Opsie', coins[i])

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

if __name__ == "__main__":
    create_coin()

    parse_coin()
