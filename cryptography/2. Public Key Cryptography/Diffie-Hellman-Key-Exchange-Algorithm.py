"""
The Diffie-Hellman Key Exchange algorithm is a cryptographic protocol that allows two parties to establish a shared 
secret key over an insecure communication channel, without any prior knowledge of each other. This shared key can 
then be used to encrypt and decrypt messages between the two parties.

Here's how the Diffie-Hellman Key Exchange algorithm works:

1. Public Parameter Generation:
   - The two parties agree on two public parameters: a prime number `p` and a generator `g` (a number less than `p` 
   that has the property that every number from 1 to `p-1` can be expressed as a power of `g` modulo `p`).

2. Private Key Generation:
   - Party A chooses a private key `a`, which is a random integer between 1 and `p-1`.
   - Party B chooses a private key `b`, which is a random integer between 1 and `p-1`.

3. Public Key Computation:
   - Party A computes its public key `A = g^a mod p`.
   - Party B computes its public key `B = g^b mod p`.

4. Key Exchange:
   - Party A sends its public key `A` to Party B.
   - Party B sends its public key `B` to Party A.

5. Shared Key Computation:
   - Party A computes the shared secret key `K = B^a mod p`.
   - Party B computes the shared secret key `K = A^b mod p`.

Both parties have now computed the same shared secret key `K`, which can be used for secure communication. The 
key `K` is computed as `K = (g^b)^a mod p = (g^a)^b mod p`, which is the same for both parties due to the 
commutative property of exponentiation.

The security of the Diffie-Hellman Key Exchange algorithm relies on the difficulty of the Discrete Logarithm 
Problem (DLP), which is the problem of finding the private key `a` or `b` given the public parameters `p`, `g`, and 
the public keys `A` or `B`. The DLP is considered a hard problem, and it is believed that there is no efficient 
algorithm to solve it in a reasonable amount of time.

The Diffie-Hellman Key Exchange algorithm is widely used in various cryptographic protocols, such as SSL/TLS, 
IPsec, and SSH, to establish secure communication channels between parties without the need for prior shared secrets.

"""

import random

def diffie_hellman_key_exchange(p, g):
    """
    Perform Diffie-Hellman Key Exchange between two parties.

    Args:
        p (int): A large prime number.
        g (int): A generator modulo p.

    Returns:
        tuple: A tuple containing the shared secret key (int) and the public keys of both parties (int, int).
    """
    # Party A's private key
    a = random.randint(1, p-1)
    A = pow(g, a, p)

    # Party B's private key
    b = random.randint(1, p-1)
    B = pow(g, b, p)

    # Compute the shared secret key
    shared_key = pow(B, a, p)

    return shared_key, A, B

# Example usage
p = 23  # A large prime number
g = 5   # A generator modulo p

shared_key, A, B = diffie_hellman_key_exchange(p, g)
print(f"Shared secret key: {shared_key}")
print(f"Party A's public key: {A}")
print(f"Party B's public key: {B}")

"""
Here's how the code works:

1. The diffie_hellman_key_exchange() function takes two parameters: p (a large prime number) and g (a generator 
modulo p).
2. Party A generates a random private key a and computes its public key A = g^a mod p.
3. Party B generates a random private key b and computes its public key B = g^b mod p.
4. The parties exchange their public keys (A and B).
5. Each party computes the shared secret key K = B^a mod p = A^b mod p.
6. The function returns the shared secret key and the public keys of both parties.

In the example usage, we set p = 23 and g = 5, and then call the diffie_hellman_key_exchange() function to perform 
the Diffie-Hellman Key Exchange. The output shows the shared secret key and the public keys of both parties.

Note that in a real-world scenario, you would typically use much larger prime numbers and generators to ensure the 
security of the Diffie-Hellman Key Exchange.

"""