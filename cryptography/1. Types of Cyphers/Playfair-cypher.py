def prepare_key(key):
    """
    Prepares the key by removing duplicates and adding 'I' in place of 'J'.
    """
    key = key.upper().replace('J', 'I')
    result = []
    for char in key:
        if char not in result:
            result.append(char)
    return ''.join(result)

def generate_grid(key):
    """
    Generates the 5x5 Playfair grid from the prepared key.
    """
    grid = [[0 for _ in range(5)] for _ in range(5)]
    row, col = 0, 0
    for char in key:
        grid[row][col] = char
        col += 1
        if col == 5:
            col = 0
            row += 1
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if char not in key:
            grid[row][col] = char
            col += 1
            if col == 5:
                col = 0
                row += 1
    return grid

def find_in_grid(grid, char):
    """
    Finds the row and column of a character in the Playfair grid.
    """
    for i in range(5):
        for j in range(5):
            if grid[i][j] == char:
                return i, j
    return None, None

def playfair_cipher(text, key, encrypt=True):
    """
    Performs Playfair Cipher encryption or decryption on the input text.
    
    Args:
        text (str): The text to be encrypted or decrypted.
        key (str): The key for the Playfair Cipher.
        encrypt (bool): True to encrypt, False to decrypt.
    
    Returns:
        str: The encrypted or decrypted text.
    """
    result = ''
    grid = generate_grid(prepare_key(key))
    text = text.upper().replace('J', 'I')
    pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    for pair in pairs:
        if len(pair) < 2:
            pair += 'X'
        row1, col1 = find_in_grid(grid, pair[0])
        row2, col2 = find_in_grid(grid, pair[1])
        if row1 is None or col1 is None or row2 is None or col2 is None:
            result += pair
        elif row1 == row2:
            if encrypt:
                result += grid[row1][(col1 + 1) % 5] + grid[row2][(col2 + 1) % 5]
            else:
                result += grid[row1][(col1 - 1) % 5] + grid[row2][(col2 - 1) % 5]
        elif col1 == col2:
            if encrypt:
                result += grid[(row1 + 1) % 5][col1] + grid[(row2 + 1) % 5][col2]
            else:
                result += grid[(row1 - 1) % 5][col1] + grid[(row2 - 1) % 5][col2]
        else:
            result += grid[row1][col2] + grid[row2][col1]
    return result

# Example usage
plaintext = "HELLO WORLD"
key = "PLAYFAIREXAMPLE"
ciphertext = playfair_cipher(plaintext, key, encrypt=True)
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted text:", playfair_cipher(ciphertext, key, encrypt=False))


"""
The key aspects of this Playfair Cipher implementation are:

1. The `prepare_key()` function removes duplicates from the key and replaces 'J' with 'I'.
2. The `generate_grid()` function creates the 5x5 Playfair grid from the prepared key.
3. The `find_in_grid()` function locates the row and column of a character in the Playfair grid.
4. The `playfair_cipher()` function performs the actual encryption and decryption, following the Playfair Cipher rules.

In the example usage, the plaintext "HELLO WORLD" is encrypted using the Playfair Cipher with the key "PLAYFAIREXAMPLE", and the resulting ciphertext is then decrypted.

"""