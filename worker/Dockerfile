FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY callback.py .
COPY consumer.py .
COPY database.py .
COPY router_client.py .
COPY worker.py .

# Run worker
CMD ["python", "-u", "worker.py"]