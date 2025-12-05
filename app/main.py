import os
import base64
import time
import pyotp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

app = FastAPI()

SEED_FILE = "/data/seed.txt"
PRIVATE_KEY_FILE = "student_private.pem"


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def home():
    return {"message": "2FA Microservice Running"}


# -----------------------------
# Models
# -----------------------------
class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


# -----------------------------
# Helper Functions
# -----------------------------
def load_private_key():
    if not os.path.exists(PRIVATE_KEY_FILE):
        raise Exception("Private key file missing")

    with open(PRIVATE_KEY_FILE, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def decrypt_hex_seed(encrypted_seed_b64: str) -> str:
    encrypted = base64.b64decode(encrypted_seed_b64)
    private_key = load_private_key()

    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    hex_seed = decrypted.decode().strip()

    if len(hex_seed) != 64 or any(c not in "0123456789abcdef" for c in hex_seed):
        raise Exception("Invalid hex seed format")

    return hex_seed


def load_hex_seed():
    if not os.path.exists(SEED_FILE):
        raise Exception("Seed not decrypted yet")

    with open(SEED_FILE, "r") as f:
        return f.read().strip()


def generate_totp(hex_seed: str):
    secret_bytes = bytes.fromhex(hex_seed)
    base32_secret = base64.b32encode(secret_bytes).decode()
    totp = pyotp.TOTP(base32_secret)
    return totp.now()


def verify_totp(hex_seed: str, code: str):
    secret_bytes = bytes.fromhex(hex_seed)
    base32_secret = base64.b32encode(secret_bytes).decode()
    totp = pyotp.TOTP(base32_secret)
    return totp.verify(code, valid_window=1)


# -----------------------------
# Endpoint 1: POST /decrypt-seed
# -----------------------------
@app.post("/decrypt-seed")
def decrypt_seed(req: DecryptRequest):
    try:
        hex_seed = decrypt_hex_seed(req.encrypted_seed)

        os.makedirs("/data", exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)

        return {
            "status": "ok",
            "decrypted_seed": hex_seed
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")


# -----------------------------
# Endpoint 2: GET /generate-2fa
# -----------------------------
@app.get("/generate-2fa")
def generate_2fa():
    try:
        hex_seed = load_hex_seed()
        code = generate_totp(hex_seed)

        valid_for = 30 - (int(time.time()) % 30)

        return {
            "code": code,
            "valid_for": valid_for
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")


# -----------------------------
# Endpoint 3: POST /verify-2fa
# -----------------------------
@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    try:
        hex_seed = load_hex_seed()
        result = verify_totp(hex_seed, req.code)

        return {"valid": result}

    except Exception:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
