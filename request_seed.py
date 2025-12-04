import requests

STUDENT_ID = "23A91A61J6"
GITHUB_REPO_URL = "https://github.com/savinay/PKI-Based-2FA-Microservice-with-Docker-23A91A61J6"
PUBLIC_KEY_FILE = "student_public.pem"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

# Read public key with proper line breaks
with open(PUBLIC_KEY_FILE, "r") as f:
    public_key = f.read().strip()  # keep BEGIN/END and line breaks

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_REPO_URL,
    "public_key": public_key
}

response = requests.post(API_URL, json=payload)

# Save encrypted seed to a file
if response.status_code == 200:
    data = response.json()
    if data.get("status") == "success":
        with open("encrypted_seed.txt", "w") as f:
            f.write(data["encrypted_seed"])
        print("Encrypted seed saved to encrypted_seed.txt")
    else:
        print("Error from API:", data)
else:
    print("HTTP Error:", response.status_code)
