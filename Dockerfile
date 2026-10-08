FROM python:3.13-slim

WORKDIR /app

# Menjalankan container sebagai user non-root user untuk keamanana
RUN useradd -m appuser

# Upgrade build tools prior to installing app requirements
RUN python -m pip install --no-cache-dir --upgrade pip
COPY requirements.txt .

# Install dependencies directly from the updated requirements file
RUN python -m pip install --no-cache-dir \
    --upgrade-strategy eager \
    -r requirements.txt

COPY . .
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 5000
CMD ["python", "app.py"]