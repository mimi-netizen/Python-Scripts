# Function to calculate gcd
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Function to find modular inverse of e mod phi
def find_d(e, phi):
    d = 1
    while (d * e) % phi != 1:
        d += 1
    return d

# Given values
p = 13
q = 11
n = p * q  # Calculate n
phi = (p - 1) * (q - 1)  # Calculate Euler's Totient function, phi

# Public key component
e = 13

# Check that e and phi are co-prime
if gcd(e, phi) != 1:
    raise ValueError("e and phi are not co-prime. Choose a different e.")

# Find d, the modular inverse of e
d = find_d(e, phi)

print("Public key (e, n):", (e, n))
print("Private key (d, n):", (d, n))
