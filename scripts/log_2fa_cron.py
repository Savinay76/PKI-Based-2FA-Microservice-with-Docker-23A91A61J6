#!/usr/bin/env python3
import os
import base64
from datetime import datetime, timezone
import pyotp

SEED_FILE = "/data/seed.txt"

def read_seed():
    try:
        with open(SEED_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def hex_to_base32(hex_str: str) -> str:
    raw_bytes = bytes.fromhex(hex_str)
    return base64.b32encode(raw_bytes).decode("utf-8")

def main():
    seed_hex = read_seed()
    if not seed_hex:
        print("Seed not found")
        return

    try:
        seed_b32 = hex_to_base32(seed_hex)
        totp = pyotp.TOTP(seed_b32)
        code = totp.now()
    except Exception as e:
        print(f"Error generating TOTP: {e}")
        return

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
