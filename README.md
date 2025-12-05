# PKI-Based 2FA Microservice with Docker (23A91A61J6)

A complete PKI-based Two-Factor Authentication (2FA) microservice implementing secure RSA/OAEP seed decryption, TOTP generation, validation, cron automation, Docker containerization, and RSA-PSS commit proof.

This project satisfies all functional, cryptographic, Docker, cron, and submission requirements.

---

# 📁 Repository Structure

```

.
├── .gitattributes
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── encrypted_seed.txt
├── instructor_public.pem
├── README.md
├── student_private.pem
├── student_public.pem
│
├── app/
│   ├── decrypt_seed.py
│   ├── main.py
│   └── totp.py
│
├── cron/
│   └── 2fa-cron
│
├── data/
│   └── seed.txt
│
└── scripts/
├── generate_commit_proof.py
├── generate_keys.py
├── log_2fa_cron.py
└── request_seed.py

```

---

# 🔐 Core Features

## 1️⃣ RSA/OAEP Seed Decryption
- Decrypts encrypted seed received from the instructor API.
- Uses:
  - **RSA-OAEP**
  - **SHA-256**
  - **MGF1(SHA-256)**
- Stores decrypted 64-hex seed in:
```

/data/seed.txt

```
- Seed persists across container restarts using Docker volumes.

---

## 2️⃣ TOTP Generation (RFC 6238)
- Converts **Hex → Base32**.
- Generates **6-digit TOTP codes every 30 seconds**.
- UTC enforced for time accuracy.
- Endpoint: `/generate-2fa`.

---

## 3️⃣ TOTP Verification
- Verifies code with **±1 time-step tolerance** (`valid_window = 1`).
- Endpoint: `/verify-2fa`.

---

## 4️⃣ Cron Job Automation
- Runs **every minute**.
- Logs new TOTP codes with UTC timestamps into:
```

/cron/last_code.txt

````
- Cron file uses **LF** line endings (required for Linux cron).

---

## 5️⃣ Dockerized Microservice
Includes:
- Multi-stage **Dockerfile**
- FastAPI running via **Uvicorn**
- Cron daemon inside container
- Persistent Docker volumes
- Port mapping `8080:8080`

Volumes:
| Volume Name | Path |
|-------------|-------|
| seed-data | /data |
| cron-output | /cron |

---

## 6️⃣ RSA-PSS Commit Proof Generation
Script `generate_commit_proof.py` generates:
- Commit hash  
- RSA-PSS (SHA-256) signature  
- Signature encrypted using instructor public key (RSA-OAEP-SHA256)  
- Base64 output (single line)

Used for project verification.

---

# 🧪 API Endpoints

---

### 🔸 **POST /decrypt-seed**

Decrypts the instructor-provided encrypted seed.

#### **Request**
```json
{
"encrypted_seed": "BASE64_STRING"
}
````

#### **Response**

```json
{
  "status": "ok",
  "decrypted_seed": "64-character-hex"
}
```

---

### 🔸 **GET /generate-2fa**

Returns the current 6-digit TOTP code.

#### **Response**

```json
{
  "code": "123456",
  "valid_for": 20
}
```

---

### 🔸 **POST /verify-2fa**

Verifies a user-supplied TOTP code.

#### **Request**

```json
{
  "code": "123456"
}
```

#### **Response**

```json
{
  "valid": true
}
```

---

# ▶️ Running the Project

### **Build & Start Containers**

```bash
docker-compose build
docker-compose up -d
```

### **Stop Containers**

```bash
docker-compose down
```

---

# 🧪 Testing the Microservice

---

### **1️⃣ Decrypt the Seed**

```bash
curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\": \"$(cat encrypted_seed.txt)\"}"
```

---

### **2️⃣ Generate a TOTP Code**

```bash
curl http://localhost:8080/generate-2fa
```

---

### **3️⃣ Verify a Valid Code**

```bash
CODE=$(curl -s http://localhost:8080/generate-2fa | jq -r '.code')

curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"$CODE\"}"
```

---

### **4️⃣ Verify an Invalid Code**

```bash
curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"000000\"}"
```

---

### **5️⃣ Check Cron Output**

```bash
docker exec pki-2fa-service cat /cron/last_code.txt
```

---

# 📦 Docker Volumes

| Volume      | Mount Path |
| ----------- | ---------- |
| seed-data   | /data      |
| cron-output | /cron      |

These ensure decrypted seed and cron logs persist across container restarts.

---

# 🔒 Security Notes

* Keys in this repository are **for assignment use only**.
* Do **NOT** reuse these keys in real systems.
* Implements required cryptographic algorithms:

  * **RSA-OAEP-SHA256** (decryption)
  * **RSA-PSS-SHA256** (signing)
  * **RSA-OAEP-SHA256** (signature encryption)

---

# 📤 Submission Deliverables

Submit:

* GitHub repository URL
* Latest commit hash
* Base64 encrypted commit signature
* Student public key
* Encrypted seed
* Running Dockerized microservice
* Cron log output showing valid TOTP codes

---

# ✅ Completion Checklist

* ✔ Three working REST API endpoints
* ✔ RSA/OAEP-SHA256 decryption
* ✔ Correct TOTP generation
* ✔ Verification with ±1 time window
* ✔ Cron job logging every minute
* ✔ Seed persists using Docker volumes
* ✔ Multi-stage Dockerfile implemented
* ✔ docker-compose.yml configured correctly
* ✔ RSA-PSS commit proof working
* ✔ All required files committed
* ✔ `.gitattributes` ensures LF endings
* ✔ All functional tests passed