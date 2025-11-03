FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY database.py .
COPY producer.py .
COPY scheduler.py .

# Run scheduler
CMD ["python", "-u", "scheduler.py"]