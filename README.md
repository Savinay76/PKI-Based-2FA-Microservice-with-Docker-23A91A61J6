# PKI-Based-2FA-Microservice-with-Docker-23A91A61J6

This project implements a complete PKI-based Two-Factor Authentication (2FA) microservice supporting RSA/OAEP seed decryption, TOTP generation, 2FA verification, cron automation, Docker containerization, and RSA-PSS commit proof generation.

All requirements of the assignment are implemented and verified.

---

## Features

### 1. RSA/OAEP Seed Decryption
- Accepts encrypted seed from instructor API.
- Decrypts using RSA-OAEP with SHA-256 and MGF1(SHA-256).
- Stores decrypted 64-character hex seed into `/data/seed.txt` using a persistent Docker volume.

### 2. TOTP Generation (RFC 6238)
- Converts hex seed into Base32.
- Generates valid 6-digit TOTP codes (30-second interval).
- Enforces UTC timezone for accuracy.
- Available at `/generate-2fa`.

### 3. TOTP Verification
- Verifies user-supplied TOTP codes.
- Allows ±1 time-step tolerance (`valid_window=1`).
- Available at `/verify-2fa`.

### 4. Cron Job Execution
A cron job runs every minute and logs a new TOTP code into:

/cron/last_code.txt

markdown
Copy code

Cron file uses LF line endings (Linux-compatible).

### 5. Dockerized Environment
- Multi-stage Dockerfile for optimized image size.
- FastAPI server via Uvicorn.
- Cron daemon inside container.
- Persistent volumes for seed and cron logs.
- Port mapping: **8080:8080**.
- Mounted key files for cryptographic operations.

### 6. Docker Compose Setup
- Defines service, volumes, and environment variables.
- Ensures persistence across restarts.
- Enforces UTC timezone.

### 7. RSA-PSS Commit Proof
A Python script generates:
- Commit hash
- RSA-PSS-SHA256 signature
- Encrypted signature using instructor public key
- Base64-encoded final proof

---

## Repository Structure

├── main.py
├── totp.py
├── request_seed.py
├── decrypt_seed.py
├── generate_commit_proof.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── cron/
│ └── 2fa-cron
├── scripts/
│ └── log_2fa_cron.py
├── student_private.pem
├── student_public.pem
├── instructor_public.pem
├── encrypted_seed.txt
├── .gitattributes
└── .gitignore

pgsql
Copy code

---

## 🚀 API Endpoints

---

### **POST /decrypt-seed**
- Decrypts the encrypted seed using RSA-OAEP-SHA256.
- Stores the decrypted 64-character hex seed in `/data/seed.txt`.

**Request**
```json
{
  "encrypted_seed": "BASE64_STRING"
}
Response

json
Copy code
{
  "status": "ok",
  "decrypted_seed": "64-character-hex"
}
GET /generate-2fa
Generates a valid 6-digit TOTP code (RFC 6238).

Uses UTC time.

Returns remaining validity time in seconds.

Response

json
Copy code
{
  "code": "123456",
  "valid_for": 20
}
POST /verify-2fa
Verifies a submitted TOTP code.

Accepts ±30s time window (valid_window = 1).

Request

json
Copy code
{
  "code": "123456"
}
Response

json
Copy code
{
  "valid": true
}
🏃 Running the Project
Start the Service
bash
Copy code
docker-compose build
docker-compose up -d
Stop the Service
bash
Copy code
docker-compose down
🧪 Testing the Endpoints
1. Decrypt the Seed
bash
Copy code
curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\": \"$(cat encrypted_seed.txt)\"}"
2. Generate TOTP
bash
Copy code
curl http://localhost:8080/generate-2fa
3. Verify Valid Code
bash
Copy code
CODE=$(curl -s http://localhost:8080/generate-2fa | jq -r '.code')

curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"$CODE\"}"
4. Verify Invalid Code
bash
Copy code
curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"000000\"}"
5. Check Cron Output
bash
Copy code
docker exec pki-2fa-service cat /cron/last_code.txt
📦 Docker Volumes
seed-data → /data (persists decrypted seed)

cron-output → /cron (stores cron-generated TOTP log)

🔒 Security Notes
Keys included are for assignment use only.

Do not reuse these keys in any real system.

Required crypto algorithms:

RSA-OAEP-SHA256 (decryption)

RSA-PSS-SHA256 (signing)

RSA-OAEP-SHA256 (signature encryption)

📤 Submission Deliverables
GitHub Repository URL

Commit Hash

Encrypted Commit Signature (Base64, single line)

Student Public Key

Encrypted Seed

Working Dockerized Microservice

Cron Output

✔ Completed Requirements Checklist
Functional 2FA microservice (3 endpoints)

RSA/OAEP-SHA256 decryption working

TOTP generation & verification correct

Cron job logs codes every minute

Seed persists using Docker volumes

Multi-stage Dockerfile implemented

docker-compose configured correctly

RSA-PSS commit proof implemented

All required files committed

Correct .gitattributes + .gitignore

Full testing completed successfully