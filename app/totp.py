import time
import hmac
import hashlib
import base64


def generate_totp(secret: str, interval: int = 30, digits: int = 6) -> str:
    key = base64.b32encode(secret.encode())
    counter = int(time.time() / interval)
    msg = counter.to_bytes(8, "big")

    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code = (int.from_bytes(h[offset:offset + 4], "big") & 0x7fffffff) % (10 ** digits)

    return str(code).zfill(digits)
