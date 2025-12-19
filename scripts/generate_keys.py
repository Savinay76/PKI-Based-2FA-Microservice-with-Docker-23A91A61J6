from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_keypair(key_size: int = 4096):
    """
    Generate RSA key pair

    Returns:
        Tuple of (private_key, public_key) objects
    """
    # 1. Generate the private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,   # standard requirement
        key_size=key_size,       # 4096 bits for assignment
    )

    # 2. Derive public key
    public_key = private_key.public_key()

    return private_key, public_key


def main():
    # Generate keypair
    private_key, public_key = generate_rsa_keypair()

    # Serialize private key (unencrypted PKCS8)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Save files
    with open("student_private.pem", "wb") as f:
        f.write(private_pem)

    with open("student_public.pem", "wb") as f:
        f.write(public_pem)

    print("✅ Generated student_private.pem and student_public.pem")


if __name__ == "__main__":
    main()