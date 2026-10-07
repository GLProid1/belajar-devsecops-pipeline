FROM python:3.13-slim

WORKDIR /app

RUN useradd -m appuser

# Upgrade build tools prior to installing app requirements
RUN python -m pip install --no-cache-dir --upgrade pip setuptools>=78.1.1 wheel>=0.46.2

COPY requirements.txt .

# Install dependencies directly from the updated requirements file
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

# Remove the manifest inside the image if not needed at runtime
RUN rm -f requirements.txt

RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 5000
CMD ["python", "app.py"]