def keyless_transposition_cipher(text, encrypt=True):
    """
    Performs Keyless Transposition Cipher encryption or decryption on the input text.
    
    Args:
        text (str): The text to be encrypted or decrypted.
        encrypt (bool): True to encrypt, False to decrypt.
    
    Returns:
        str: The encrypted or decrypted text.
    """
    result = ''
    text_length = len(text)
    columns = int(text_length ** 0.5)
    rows = columns if text_length % columns == 0 else columns + 1
    grid = [['' for _ in range(columns)] for _ in range(rows)]

    if encrypt:
        # Fill the grid row-wise
        idx = 0
        for row in range(rows):
            for col in range(columns):
                if idx < text_length:
                    grid[row][col] = text[idx]
                    idx += 1

        # Read the grid column-wise
        for col in range(columns):
            for row in range(rows):
                if grid[row][col]:
                    result += grid[row][col]
    else:
        # Fill the grid column-wise
        idx = 0
        for col in range(columns):
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
ciphertext = keyless_transposition_cipher(plaintext, encrypt=True)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted text:", keyless_transposition_cipher(ciphertext, encrypt=False))

"""
The key aspects of this Keyless Transposition Cipher implementation are:

1. The keyless_transposition_cipher() function performs both encryption and decryption.
2. For encryption:
    - The input text is arranged in a rectangular grid, row-wise.
    - The grid is then read column-wise to generate the ciphertext.
3. For decryption:
    - The ciphertext is arranged in a rectangular grid, column-wise.
    - The grid is then read row-wise to generate the plaintext.

The size of the rectangular grid is determined by the square root of the length of the input text. If the length is 
not a perfect square, an additional row is added to accommodate the remaining characters.

In the example usage, the plaintext "HELLO WORLD" is encrypted using the Keyless Transposition Cipher, and the 
resulting ciphertext is then decrypted.

This implementation assumes that the input text contains only alphanumeric characters and spaces. 
If you need to handle other types of characters, you may need to modify the code accordingly.

"""