import base64
import time
import pyotp


def hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-char hex seed into Base32 string required by TOTP.
    """
    # Convert hex → bytes
    seed_bytes = bytes.fromhex(hex_seed)

    # Convert bytes → base32 string
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

    return base32_seed


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current 6-digit TOTP code using SHA-1, 30s period.

    Args:
        hex_seed: 64-char hex seed string

    Returns:
        6-digit TOTP code as string
    """
    base32_seed = hex_to_base32(hex_seed)

    # Create TOTP object (SHA-1, digits=6, interval=30)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # Generate current TOTP code
    return totp.now()


def generate_totp_with_validity(hex_seed: str):
    """
    Generate TOTP code + remaining validity seconds.

    Returns:
        (code, valid_for)
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # 6-digit code
    code = totp.now()

    # Remaining seconds in the current 30-sec window
    current_time = int(time.time())
    valid_for = 30 - (current_time % 30)

    return code, valid_for


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify the TOTP code using ±1 time window (±30 seconds allowed).

    Args:
        hex_seed: 64-char hex seed
        code: code to verify
        valid_window: number of periods to accept before/after (default 1)

    Returns:
        True if valid, False if invalid
    """
    base32_seed = hex_to_base32(hex_seed)

    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)

    # valid_window=1 means accept:
    # previous window, current, next window
    return totp.verify(code, valid_window=valid_window)