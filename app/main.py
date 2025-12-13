from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from app.totp import generate_totp

app = FastAPI()

DATA_DIR = "/data"
SEED_FILE = f"{DATA_DIR}/seed.txt"

os.makedirs(DATA_DIR, exist_ok=True)


class SeedRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


@app.post("/decrypt-seed")
def decrypt_seed(req: SeedRequest):
    with open(SEED_FILE, "w") as f:
        f.write(req.encrypted_seed)
    return {"status": "seed stored"}


@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=400, detail="Seed not found")

    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()

    code = generate_totp(seed)
    return {"code": code}


@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=400, detail="Seed not found")

    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()

    valid_code = generate_totp(seed)
    return {"valid": req.code == valid_code}
