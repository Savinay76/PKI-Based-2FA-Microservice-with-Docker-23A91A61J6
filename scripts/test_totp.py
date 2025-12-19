import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.totp_utils import generate_totp_code, verify_totp_code

hex_seed = "c09c109b3beb5d784cd39f7788e69d0147abebe38991323c084caf34b67fae34"

code = generate_totp_code(hex_seed)
print("Generated OTP:", code)

is_valid = verify_totp_code(hex_seed, code)
print("Is valid:", is_valid)