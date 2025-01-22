# Function to calculate gcd and extended gcd to find modular inverse
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Function to find modular inverse of e mod phi
def mod_inverse(e, phi):
    gcd, x, y = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist for these values.")
    else:
        return x % phi

# Given values
p = 7
q = 11
n = p * q  # Calculate n
phi = (p - 1) * (q - 1)  # Calculate Euler's Totient function, phi

# Choose e such that 1 < e < phi and gcd(e, phi) == 1
e = 2
while e < phi:
    if extended_gcd(e, phi)[0] == 1:
        break
    else:
        e += 1

# Compute d using the modular inverse of e mod phi
d = mod_inverse(e, phi)

# Given plaintext message to be encrypted
m = 9

# Encryption: c = (m ^ e) % n
c = pow(m, e, n)

print("Public key (e, n):", (e, n))
print("Private key (d, n):", (d, n))
print("Plaintext message:", m)
print("Encrypted ciphertext:", c)

# Decryption to verify the result: m = (c ^ d) % n
decrypted_message = pow(c, d, n)
print("Decrypted message:", decrypted_message)
