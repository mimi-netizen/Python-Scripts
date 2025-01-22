def vigenere_table():
    """
    Generates the Vigenère table.
    """
    table = [[] for _ in range(26)]
    for i in range(26):
        for j in range(26):
            table[i].append(chr((i + j) % 26 + 65))
    return table

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
    table = vigenere_table()
    key_idx = 0
    for char in text:
        if char.isalpha():
            row = ord(key.upper()[key_idx]) - 65
            col = ord(char.upper()) - 65
            if encrypt:
                result += table[row][col]
            else:
                for i in range(26):
                    if table[row][i] == char.upper():
                        result += table[0][i]
                        break
            key_idx = (key_idx + 1) % len(key)
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
The key aspects of this Vigenère Cipher implementation are:

1. The vigenere_table() function generates the 26x26 Vigenère table.
2. The vigenere_cipher() function performs the actual encryption and decryption, using the Vigenère table.
    - For each character in the input text, it finds the corresponding row and column in the Vigenère table 
        based on the current key character and the input character.
    - For encryption, it uses the value at the intersection of the row and column as the encrypted character.
    - For decryption, it loops through the column corresponding to the key character and finds the row with 
        the input character, then uses the character at the intersection of the first row and that column as the decrypted character.
    - The key index is incremented after each character is processed, wrapping around to the beginning of the key if necessary.
    
In the example usage, the plaintext "HELLO WORLD" is encrypted using the Vigenère Cipher with the key "LEMON", 
and the resulting ciphertext is then decrypted.
"""