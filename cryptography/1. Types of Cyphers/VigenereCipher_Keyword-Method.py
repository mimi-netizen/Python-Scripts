def prepare_key(key, text_length):
    """
    Prepares the key by repeating it to match the length of the text.
    """
    key = key.upper()
    return (key * (text_length // len(key)) + key[:text_length % len(key)])

def vigenere_cipher(text, key, encrypt=True):
    """
    Performs Vigenère Cipher encryption or decryption on the input text.
    
    Args:
        text (str): The text to be encrypted or decrypted.
        key (str): The key for the Vigenère Cipher.
        encrypt (bool): True to encrypt, False to decrypt.
    
    Returns:
        str: The encrypted or decrypted text.
    """
    result = ''
    key = prepare_key(key, len(text))
    for i, char in enumerate(text):
        if char.isalpha():
            row = ord(char.upper()) - 65
            col = ord(key[i]) - 65
            if encrypt:
                result += chr((row + col) % 26 + 65)
            else:
                result += chr((row - col) % 26 + 65)
        else:
            result += char
    return result

# Example usage
plaintext = "HELLO WORLD"
key = "LEMON"
ciphertext = vigenere_cipher(plaintext, key, encrypt=True)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted text:", vigenere_cipher(ciphertext, key, encrypt=False))

"""
The key aspects of this Vigenère Cipher implementation using the Keyword method are:

1. The prepare_key() function takes the key and the length of the plaintext, and generates a new key that matches the 
    length of the plaintext by repeating the key as necessary.
2. The vigenere_cipher() function performs the actual encryption and decryption.
    - For each character in the input text, it finds the corresponding row and column in the "virtual" Vigenère table 
        based on the current key character and the input character.
    - For encryption, it uses the value at the intersection of the row and column as the encrypted character.
    - For decryption, it subtracts the column value from the row value and takes the modulo 26 to get the decrypted 
        character.
    - The key index is incremented after each character is processed, wrapping around to the beginning of the key 
        if necessary.
        
In the example usage, the plaintext "HELLO WORLD" is encrypted using the Vigenère Cipher with the key "LEMON", and the 
resulting ciphertext is then decrypted.

The main difference between this implementation and the "Vigenère Table Method" is that this one doesn't use the Vigenère table 
directly, but instead calculates the encrypted/decrypted character by using the row and column values based on the input character 
and the key character.

"""