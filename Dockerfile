FROM python:3.13-slim

WORKDIR /app

# Menjalankan container dengan non-root user demi keamanan runtime
RUN useradd -m appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m pip install --no-cache-dir --upgrade \
        "setuptools==78.1.1" \
        "urllib3==2.8.0" \
        "msgpack==1.2.1"

COPY . .
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 5000
CMD ["python", "app.py"]