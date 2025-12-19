import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.crypto_utils import load_private_key, decrypt_seed

private_key = load_private_key()
encrypted_seed = open("encrypted_seed.txt").read().strip()

hex_seed = decrypt_seed(encrypted_seed, private_key)
print("Decrypted seed =", hex_seed)
print("Length =", len(hex_seed))