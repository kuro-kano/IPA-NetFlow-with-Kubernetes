import os
import sys
import time
import pika
from callback import callback


def consume(host):
    """Consume jobs from RabbitMQ"""
    user = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
    pwd = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
    worker_id = os.getenv("WORKER_ID", "unknown")

    print(f"Worker #{worker_id} starting...")
    print(f"RabbitMQ host: {host}")
    print(f"Username: {user}")

    max_retries = 15
    retry_delay = 5

    conn = None

    for attempt in range(1, max_retries + 1):
        try:
            print(f"\nConnecting to RabbitMQ (attempt {attempt}/{max_retries})...")

            creds = pika.PlainCredentials(user, pwd)
            params = pika.ConnectionParameters(
                host=host,
                credentials=creds,
                heartbeat=600,
                blocked_connection_timeout=300,
            )

            conn = pika.BlockingConnection(params)
            print(f"Successfully connected to RabbitMQ!")
            break

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection failed: {e}")

            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Could not connect after {max_retries} attempts")
                sys.exit(1)

        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(retry_delay)

    if conn is None:
        print("Failed to establish connection")
        sys.exit(1)

    try:
        ch = conn.channel()
        ch.queue_declare(queue="router_jobs", durable=True)
        ch.basic_qos(prefetch_count=1)

        print(f"\n{'='*60}")
        print(f"Worker #{worker_id} is ready to receive jobs")
        print(f"{'='*60}\n")

        ch.basic_consume(
            queue="router_jobs", on_message_callback=callback, auto_ack=False
        )

        ch.start_consuming()

    except KeyboardInterrupt:
        print("\nWorker stopped by user")
        if conn and not conn.is_closed:
            conn.close()
        sys.exit(0)

    except Exception as e:
        print(f"Error in consumer: {e}")
        if conn and not conn.is_closed:
            conn.close()
        sys.exit(1)
