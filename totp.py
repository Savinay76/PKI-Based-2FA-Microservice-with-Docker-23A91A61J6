import base64
import pyotp

def hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-char hex seed → bytes → base32 string.
    """
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")
    return base32_seed


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current 6-digit TOTP using SHA-1, 30 sec period.
    """
    base32_seed = hex_to_base32(hex_seed)

    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.now()   # returns a 6-digit string


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with ± valid_window (default ±30s).
    """
    base32_seed = hex_to_base32(hex_seed)

    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.verify(code, valid_window=valid_window)


# -------------------------------
# Optional manual test
# -------------------------------
if __name__ == "__main__":
    with open("data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    current_code = generate_totp_code(hex_seed)
    print("Current TOTP:", current_code)

    print("Verification:", verify_totp_code(hex_seed, current_code))
