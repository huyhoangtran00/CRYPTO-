from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

# Step 1: Generate private and public keys (using SECP521R1)
private_key = ec.generate_private_key(ec.SECP521R1(), default_backend())  # Private key
public_key = private_key.public_key()  # Public key

# Step 2: Define the message
message = b"lopmatmavaantoanthongtinnambatoancacsieunhan"

# Step 3: Sign the message
signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))

# Step 4: Verify the signature
is_valid = public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))

# Convert keys to decimal format
private_key_decimal = private_key.private_numbers().private_value
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint,
)
public_key_decimal = int.from_bytes(
    public_key_bytes[1:], byteorder="big"
)  # Skip the first byte (0x04)

# Convert signature to a string of letters (cipher text)
cipher_text = "".join(chr(b % 26 + 97) for b in signature)  # Map bytes to letters (a-z)

# Output results
print("Private Key", private_key_decimal)
print("Public Key:", public_key_decimal)
print("Message:", message.decode())
print("Signature:", cipher_text)
