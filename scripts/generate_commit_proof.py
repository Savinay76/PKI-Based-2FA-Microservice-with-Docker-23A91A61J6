#!/usr/bin/env python3
import subprocess
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

# ----------------------------------------------------
# Load commit hash from git
# ----------------------------------------------------
def get_commit_hash():
    result = subprocess.run(["git", "log", "-1", "--format=%H"], capture_output=True, text=True)
    commit_hash = result.stdout.strip()
    if len(commit_hash) != 40:
        raise ValueError("Invalid commit hash length.")
    return commit_hash


# ----------------------------------------------------
# RSA-PSS SHA256 signature
# ----------------------------------------------------
def sign_message(message: str, private_key) -> bytes:
    return private_key.sign(
        message.encode("utf-8"),  # CRITICAL: ASCII string, NOT hex bytes
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )


# ----------------------------------------------------
# Encrypt using instructor public key (OAEP-SHA256)
# ----------------------------------------------------
def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


# ----------------------------------------------------
# Main proof generator
# ----------------------------------------------------
def main():
    # 1. Get commit hash
    commit_hash = get_commit_hash()
    print("Commit Hash:", commit_hash)

    # 2. Load student private key
    with open("student_private.pem", "rb") as f:
        student_private_key = load_pem_private_key(f.read(), password=None)

    # 3. Sign commit hash
    signature = sign_message(commit_hash, student_private_key)

    # 4. Load instructor public key
    with open("instructor_public.pem", "rb") as f:
        instructor_public_key = load_pem_public_key(f.read())

    # 5. Encrypt the signature
    encrypted_sig = encrypt_with_public_key(signature, instructor_public_key)

    # 6. Base64 encode
    encoded = base64.b64encode(encrypted_sig).decode("utf-8")

    print("\nEncrypted Signature:\n")
    print(encoded)
    print("\n--- END OF PROOF ---\n")


if __name__ == "__main__":
    main()
