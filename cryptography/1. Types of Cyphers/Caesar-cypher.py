def caesar_cipher(text, shift, encrypt=True):
    """
    Performs a Caesar cipher encryption or decryption on the input text.
    
    Args:
        text (str): The text to be encrypted or decrypted.
        shift (int): The number of positions to shift the alphabet.
        encrypt (bool): True to encrypt, False to decrypt.
    
    Returns:
        str: The encrypted or decrypted text.
    """
    result = ''
    for char in text:
        if char.isalpha():
            # Shift the character by the specified amount
            shifted = ord(char) + (shift if encrypt else -shift)
            
            # Wrap around if the character goes beyond the alphabet
            if char.isupper():
                result += chr((shifted - 65) % 26 + 65)
            else:
                result += chr((shifted - 97) % 26 + 97)
        else:
            result += char
    return result

# Example usage
plaintext = "HELLO WORLD"
shift = 3
ciphertext = caesar_cipher(plaintext, shift, encrypt=True)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted text:", caesar_cipher(ciphertext, shift, encrypt=False))

"""
This implementation takes in the text to be encrypted or decrypted, the number of positions to shift the alphabet, and a boolean flag to specify whether to encrypt or decrypt. 
It then loops through each character in the input text, shifts the character by the specified amount, and wraps around the alphabet if necessary. 
The resulting encrypted or decrypted text is returned.
"""