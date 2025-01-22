# Diffie-Hellman Code
# Power function to return value of a^b mod P
def power(a, b, p):
 if b == 1:
    return a
 else:
    return pow(a, b) % p
# Main function
def main():
 # Both persons agree upon the public keys G and P
 # A prime number P is taken
 P = 23
 print("The value of P:", P)
 # A primitive root for P, G is taken
 G = 9
 print("The value of G:", G)
# Alice chooses the private key a
 # a is the chosen private key
 a = 4
 print("The private key a for Alice:", a)
 # Gets the generated key
 x = power(G, a, P)
 # Bob chooses the private key b
 # b is the chosen private key
 b = 3
 print("The private key b for Bob:", b)
 # Gets the generated key
 y = power(G, b, P)
# Generating the secret key after the exchange of keys
 ka = power(y, a, P) # Secret key for Alice
 kb = power(x, b, P) # Secret key for Bob
 print("Secret key for Alice is:", ka)
 print("Secret key for Bob is:", kb)
if __name__ == "__main__":
 main()
 
 """
 
1. The `power()` function is a helper function that calculates the value of `a^b mod P` efficiently using the 
`pow()` function.
2. The `main()` function is the main entry point of the program.
3. Inside the `main()` function:
   - The public parameters `P` (a prime number) and `G` (a primitive root modulo `P`) are defined.
   - Alice chooses her private key `a`, and her public key `x` is computed as `G^a mod P`.
   - Bob chooses his private key `b`, and his public key `y` is computed as `G^b mod P`.
   - Alice and Bob then compute the shared secret key using their private keys and the other party's public key:
     - Alice computes `ka = y^a mod P`.
     - Bob computes `kb = x^b mod P`.
   - The shared secret keys `ka` and `kb` are printed, which should be the same for both Alice and Bob.
 
 """