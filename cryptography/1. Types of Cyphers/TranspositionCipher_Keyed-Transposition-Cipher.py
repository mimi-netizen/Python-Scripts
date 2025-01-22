def prepare_key(key):
    """
    Prepares the key by removing duplicates and sorting the characters.
    """
    key = ''.join(sorted(set(key.upper())))
    return key

def keyed_transposition_cipher(text, key, encrypt=True):
    """
    Performs Keyed Transposition Cipher encryption or decryption on the input text.
    
    Args:
        text (str): The text to be encrypted or decrypted.
        key (str): The key for the Keyed Transposition Cipher.
        encrypt (bool): True to encrypt, False to decrypt.
    
    Returns:
        str: The encrypted or decrypted text.
    """
    result = ''
    key = prepare_key(key)
    text_length = len(text)
    columns = len(key)
    rows = text_length // columns + (text_length % columns > 0)
    grid = [['' for _ in range(columns)] for _ in range(rows)]

    if encrypt:
        # Fill the grid row-wise
        idx = 0
        for row in range(rows):
            for col in range(columns):
                if idx < text_length:
                    grid[row][col] = text[idx]
                    idx += 1

        # Read the grid based on the key
        for char in key:
            col = key.index(char)
            for row in range(rows):
                if grid[row][col]:
                    result += grid[row][col]
    else:
        # Fill the grid based on the key
        idx = 0
        for char in key:
            col = key.index(char)
            for row in range(rows):
                if idx < text_length:
                    grid[row][col] = text[idx]
                    idx += 1

        # Read the grid row-wise
        for row in range(rows):
            for col in range(columns):
                if grid[row][col]:
                    result += grid[row][col]

    return result

# Example usage
plaintext = "HELLO WORLD"
key = "SECURITY"
ciphertext = keyed_transposition_cipher(plaintext, key, encrypt=True)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted text:", keyed_transposition_cipher(ciphertext, key, encrypt=False))

"""
The key aspects of this Keyed Transposition Cipher implementation are:

1. The prepare_key() function removes duplicates from the key and sorts the characters.
2. The keyed_transposition_cipher() function performs both encryption and decryption.
3. For encryption:
    The input text is arranged in a rectangular grid, row-wise.
    The grid is then read based on the order of the characters in the prepared key.
4. For decryption:
    The ciphertext is arranged in a rectangular grid based on the order of the characters in the prepared key.
    The grid is then read row-wise to generate the plaintext.
    
The size of the rectangular grid is determined by the length of the input text and the length of the prepared key. 
The number of rows is calculated as the integer division of the text length by the key length, plus an additional 
row if there are any remaining characters.

In the example usage, the plaintext "HELLO WORLD" is encrypted using the Keyed Transposition Cipher with the key 
"SECURITY", and the resulting ciphertext is then decrypted.

This implementation assumes that the input text contains only alphanumeric characters and spaces. 
If you need to handle other types of characters, you may need to modify the code accordingly.

"""