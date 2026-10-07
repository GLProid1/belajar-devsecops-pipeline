# --- Stage 1: Build & Wheel Creation ---
FROM python:3.13-slim AS builder

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip setuptools>=78.1.1 wheel>=0.46.2

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# --- Stage 2: Clean Final Image ---
FROM python:3.13-slim AS runner

WORKDIR /app

RUN useradd -m appuser

# Upgrade base tools and purge stale metadata
RUN python -m pip install --no-cache-dir --upgrade \
    "setuptools>=78.1.1" \
    "wheel>=0.46.2" \
    "jaraco.context>=6.1.0"

COPY --from=builder /app/wheels /wheels
COPY requirements.txt .

RUN python -m pip install --no-cache-dir /wheels/*

COPY . .
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 5000
CMD ["python", "app.py"]