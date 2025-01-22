The RSA (Rivest-Shamir-Adleman) algorithm is a widely used public-key cryptographic algorithm for secure communication. It is based on the mathematical concept of modular arithmetic and the difficulty of factoring large prime numbers.

Here's a step-by-step explanation of the RSA algorithm:

1. **Key Generation**:

   - Choose two large prime numbers, `p` and `q`.
   - Compute the modulus `n = p * q`.
   - Compute the totient function `φ(n) = (p-1) * (q-1)`.
   - Choose a public exponent `e` such that `1 < e < φ(n)` and `gcd(e, φ(n)) = 1` (e is relatively prime to φ(n)).
   - Compute the private exponent `d` such that `(d * e) mod φ(n) = 1` (d is the multiplicative inverse of e modulo φ(n)).

2. **Encryption**:

   - The public key is the pair `(e, n)`.
   - To encrypt a message `M`, where `0 ≤ M < n`, the ciphertext `C` is computed as `C = M^e mod n`.

3. **Decryption**:
   - The private key is the pair `(d, n)`.
   - To decrypt the ciphertext `C`, the plaintext `M` is computed as `M = C^d mod n`.

The security of the RSA algorithm relies on the difficulty of factoring large composite numbers (the product of two large prime numbers, `n = p * q`). It is believed that there is no efficient algorithm to factor large integers in a reasonable amount of time, making the RSA algorithm secure for practical applications.

Here's an example implementation of the RSA algorithm in Python:

```python
import random
import math

def gcd(a, b):
    """
    Computes the greatest common divisor of two integers.
    """
    while b != 0:
        a, b = b, a % b
    return a

def find_modular_inverse(a, m):
    """
    Finds the modular inverse of 'a' modulo 'm'.
    """
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def generate_keys(p, q):
    """
    Generates the public and private keys for the RSA algorithm.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(1, phi)
    while gcd(e, phi) != 1:
        e = random.randint(1, phi)
    d = find_modular_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(message, public_key):
    """
    Encrypts the message using the public key.
    """
    e, n = public_key
    return pow(message, e, n)

def decrypt(ciphertext, private_key):
    """
    Decrypts the ciphertext using the private key.
    """
    d, n = private_key
    return pow(ciphertext, d, n)

# Example usage
p, q = 61, 53
public_key, private_key = generate_keys(p, q)
print("Public key:", public_key)
print("Private key:", private_key)

message = 123
ciphertext = encrypt(message, public_key)
print("Encrypted message:", ciphertext)
decrypted_message = decrypt(ciphertext, private_key)
print("Decrypted message:", decrypted_message)
```

This implementation includes functions for key generation, encryption, and decryption. The `generate_keys()` function generates the public and private keys based on the two large prime numbers `p` and `q`. The `encrypt()` and `decrypt()` functions perform the RSA encryption and decryption operations, respectively.

In the example usage, the program generates the public and private keys, encrypts a message, and then decrypts the ciphertext, demonstrating the complete RSA algorithm.
