FROM python:3.12-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# We call uvicorn directly. 
# The '--forwarded-allow-ips "*"' and '--proxy-headers' are the keys here.
# We also use the module path 'scripts.voice_server:app'
CMD ["uvicorn", "scripts.voice_server:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*"]