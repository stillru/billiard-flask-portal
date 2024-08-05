#!/usr/bin/env python3
"""Utility that generates Ed25519 key and a JWT for testing

The public key is stored in jwt_key.pem (in PEM format) and jwt_key.base64 (raw
base64 format) and the JWT is printed to stdout.
"""
import base64
import datetime
import json
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

# Generate Ed25519 key pair
privkey = Ed25519PrivateKey.generate()
pubkey = privkey.public_key()

# Serialize public key to PEM format
pubkey_pem = pubkey.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

# Serialize public key to base64 format
pubkey_base64 = base64.b64encode(
    pubkey.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ),
    altchars=b"-_"
).decode('utf-8')

# Remove padding characters from the base64 string
pubkey_base64 = pubkey_base64.rstrip('=')

# Serialize private key to PEM format
privkey_pem = privkey.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
).decode('utf-8')

# Create JWT claims
exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
claims = {
    "exp": int(exp.timestamp()),
}

# Manually create JWT header
header = {
    "alg": "EdDSA",
    "typ": "JWT"
}

# Encode header and payload to base64
header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=').decode('utf-8')
payload_b64 = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b'=').decode('utf-8')

# Create the unsigned token
unsigned_token = f"{header_b64}.{payload_b64}"

# Sign the token
signature = privkey.sign(unsigned_token.encode())

# Encode signature to base64
signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b'=').decode('utf-8')

# Construct the JWT
token = f"{unsigned_token}.{signature_b64}"

# Add read-only claim and generate read-only token
claims["a"] = "ro"
payload_b64_ro = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b'=').decode('utf-8')
unsigned_token_ro = f"{header_b64}.{payload_b64_ro}"
signature_ro = privkey.sign(unsigned_token_ro.encode())
signature_b64_ro = base64.urlsafe_b64encode(signature_ro).rstrip(b'=').decode('utf-8')
ro_token = f"{unsigned_token_ro}.{signature_b64_ro}"

# Save public key to files
with open("jwt_key.pem", "wb") as pem_file:
    pem_file.write(pubkey_pem)

with open("jwt_key.base64", "w") as base64_file:
    base64_file.write(pubkey_base64)

# Print the generated tokens
print(f"Full access: {token}")
print(f"Read-only:   {ro_token}")
