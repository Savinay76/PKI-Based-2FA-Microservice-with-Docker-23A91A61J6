from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

app = FastAPI()

class SeedRequest(BaseModel):
    encrypted_seed: str

@app.post("/decrypt-seed")
def decrypt_seed(req: SeedRequest):
    # Load private key
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # Decode base64
    encrypted_bytes = base64.b64decode(req.encrypted_seed)

    # Decrypt
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    decrypted_seed = decrypted_bytes.decode()

    return {
        "status": "ok",
        "decrypted_seed": decrypted_seed
    }
