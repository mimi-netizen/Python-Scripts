# CMAC

CMAC (Cipher-based Message Authentication Code) is a cryptographic algorithm used to generate a Message Authentication Code (MAC) based on a block cipher, such as AES (Advanced Encryption Standard).

The key features and properties of CMAC are:

1. **Block Cipher-Based**: CMAC uses a block cipher, such as AES, as the underlying cryptographic primitive, unlike HMAC, which is based on a cryptographic hash function.

2. **Operational Modes**: CMAC follows the Cipher Block Chaining (CBC) mode of operation to generate the MAC.

3. **Key Generation**: CMAC uses a single secret key to generate the MAC. This key is used to derive two subkeys (K1 and K2) that are used in the MAC computation.

4. **MAC Computation**: The CMAC algorithm processes the input message in blocks, applying the block cipher and the derived subkeys to produce the final MAC value.

The CMAC algorithm works as follows:

1. **Key Derivation**:

   - The secret key is used to derive two subkeys, K1 and K2, using a specific algorithm defined in the CMAC standard.

2. **Padding**:

   - The input message is padded with a specific padding scheme to ensure that the message length is a multiple of the block size of the underlying block cipher.

3. **CBC-MAC Computation**:
   - The padded message is processed in blocks using the block cipher in Cipher Block Chaining (CBC) mode.
   - The final block cipher output is the CMAC value.

The CMAC algorithm provides the following security properties:

- **Integrity**: The CMAC value ensures that the message has not been tampered with during transmission.
- **Authentication**: The CMAC value allows the recipient to verify the authenticity of the message, i.e., that it originated from the expected sender.
- **Confidentiality**: CMAC does not provide confidentiality on its own, but it can be used in conjunction with a block cipher to provide both authentication and confidentiality.

CMAC is widely used in various applications, such as secure communication protocols (e.g., TLS, IPsec), payment systems, and data integrity checks. It is standardized by NIST (National Institute of Standards and Technology) and is considered a secure and efficient MAC algorithm.

Here's a simple example of CMAC implementation in Python using the PyCryptodome library:

```python
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import CMAC

def compute_cmac(message, key):
    """
    Compute the CMAC of the given message and key.
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    return CMAC(cipher, message.encode('utf-8')).hex()

# Example usage
message = "Hello, World!"
key = "secret_key_123"
cmac = compute_cmac(message, key)
print("Message:", message)
print("CMAC:", cmac)
```

In this example, the `compute_cmac()` function takes a message and a secret key as input, and returns the CMAC value as a hexadecimal string.
