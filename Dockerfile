# ============================================================
# Stage 1: Builder
# ============================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn pyotp cryptography


# ============================================================
# Stage 2: Runtime Image
# ============================================================
FROM python:3.11-slim

WORKDIR /app

ENV TZ=UTC

RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    && ln -fs /usr/share/zoneinfo/UTC /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies from builder
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . /app

# Create folders
RUN mkdir -p /data /cron

# ==========================
# Install CRON JOB
# ==========================
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Correct permissions
RUN chmod 0644 /etc/cron.d/2fa-cron \
    && crontab /etc/cron.d/2fa-cron

# Expose port
EXPOSE 8080

# Start cron + API
CMD cron && uvicorn main:app --host 0.0.0.0 --port 8080
