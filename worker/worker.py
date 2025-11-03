# worker.py
import os
import sys
from consumer import consume

def main():
    """
    Worker main entry point
    """
    worker_id = os.getenv("WORKER_ID", "unknown")
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq-svc")
    
    print("=" * 60)
    print(f"🔧 NetFlow Worker #{worker_id}")
    print("=" * 60)
    print(f"RabbitMQ Host: {rabbitmq_host}")
    print(f"MongoDB URI: {os.getenv('MONGO_URI', 'Not set')}")
    print(f"Database: {os.getenv('DB_NAME', 'Not set')}")
    print("=" * 60)
    
    try:
        consume(rabbitmq_host)
    except KeyboardInterrupt:
        print("\n👋 Worker shutdown requested")
        sys.exit(0)
    except Exception as e:
        print(f"\n💀 Worker crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()