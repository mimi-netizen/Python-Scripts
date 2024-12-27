# import the cryptography library
import cryptography

# use a symmetric method encryption
from cryptography.fernet import Fernet

# generate a key
key = Fernet.generate_key()

# create a Fernet object
cipher = Fernet(key)

# the message we want to encrypt
message = "This is a secret message".encode()
print("Original message:", message.decode())

# encrypt the message
encrypted_message = cipher.encrypt(message)
print("Secret message ", encrypted_message.decode())
