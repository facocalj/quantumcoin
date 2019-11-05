from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit

# Default coin size
coin_size = 4
# Global coin container
coins = []
# Global qubit pair container
pairs = []

default_offset = 1000

def create_coin(k=1):
    print("Creating the random number sequence:")
    with CQCConnection("Alice") as Alice:
        # For each K-th coin
        for i in range(k):
            # Create a new empty coin
            coins.append([None] * coin_size)
            # Create a new qubit container
            pairs.append([None] * int(0.5 * coin_size))

            # Create its P register
            P = default_offset + k
            # Iterate over the newly created coin
            for j in range(coin_size):
                # Create random bit
                random_bit = randint(0,1)
                # Assign random bit to the coin container
                coins[i][j] = random_bit

            print(coins[i])

            print('Creating qubits')
            # Create qubits: |0>
            q1 = qubit(Alice)
            q2 = qubit(Alice)

            print('Modulating qubits:')
            # Encode coins into qubits
            for index, q in enumerate([q1, q2]):
                offset = int(2 * index)
                if coins[i][0+offset:2+offset] == [0,0]:
                    # |0>
                    print('Qubit', index+1, 'Encode: |0>' )
                    #pass

                elif coins[i][0+offset:2+offset] == [0,1]:
                    # |1>
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

            print('Done!')

            m1 = q1.measure()
            m2 = q2.measure()
            print(m1)
            print(m2)
            #  Alice.sendQubit(q, "Bob")

        Alice.flush()


if __name__ == "__main__":
    create_coin()
