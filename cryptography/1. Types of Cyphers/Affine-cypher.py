import math

def gcd(a, b):
    """
    Compute the Greatest Common Divisor (GCD) of two integers.
    """
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """
    Compute the modular inverse of a modulo m.
    """
    if gcd(a, m) != 1:
        return None
    
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    
    return u1 % m

def affine_cipher(text, a, b, encrypt=True):
    """
    Performs an Affine Cipher encryption or decryption on the input text.
    
    Args:
        text (str): The text to be encrypted or decrypted.
        a (int): The multiplicative factor (must be coprime to 26).
        b (int): The additive factor.
        encrypt (bool): True to encrypt, False to decrypt.
    
    Returns:
        str: The encrypted or decrypted text.
    """
    result = ''
    for char in text:
        if char.isalpha():
            # Shift the character by the specified amount
            x = ord(char.upper()) - 65
            if encrypt:
                y = (a * x + b) % 26
            else:
                a_inv = mod_inverse(a, 26)
                y = (a_inv * (x - b)) % 26
            result += chr(y + 65)
        else:
            result += char
    return result

# Example usage
plaintext = "HELLO WORLD"
a, b = 5, 8
ciphertext = affine_cipher(plaintext, a, b, encrypt=True)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted text:", affine_cipher(ciphertext, a, b, encrypt=False))


"""

The key aspects of this Affine Cipher implementation are:

1. The `gcd()` function computes the Greatest Common Divisor (GCD) of two integers, which is used to ensure the multiplicative factor `a` is coprime to 26.
2. The `mod_inverse()` function calculates the modular inverse of `a` modulo 26, which is used in the decryption process.
3. The `affine_cipher()` function performs the actual encryption and decryption, using the provided multiplicative factor `a` and additive factor `b`.

In the example usage, the plaintext "HELLO WORLD" is encrypted using the Affine Cipher with `a=5` and `b=8`, and the resulting ciphertext is then decrypted.

"""