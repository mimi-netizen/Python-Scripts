# Function to calculate gcd and extended gcd to find modular inverse
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Function to find e using the modular inverse of d mod phi
def find_e(d, phi):
    gcd, e, _ = extended_gcd(d, phi)
    if gcd != 1:
        raise ValueError("No modular inverse found; e and phi are not coprime.")
    return e % phi

# Given values
p = 7
q = 17
d = 23
c = 12

# Step 1: Calculate n
n = p * q

# Step 2: Calculate phi
phi = (p - 1) * (q - 1)

# Step 3: Find e such that (e * d) % phi = 1
e = find_e(d, phi)

# Step 4: Decrypt the ciphertext to find the plaintext
m = pow(c, d, n)

print("Public key (e, n):", (e, n))
print("Private key (d, n):", (d, n))
print("Ciphertext:", c)
print("Decrypted Plaintext:", m)
