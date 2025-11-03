# producer.py
import os
import pika
import time

def produce(host, body):
    """produce message to RabbitMQ"""
    rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
    rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
    
    if not host:
        raise ValueError("RabbitMQ host is required")
    
    max_retries = 5
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
            parameters = pika.ConnectionParameters(
                host=host,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            
            channel.exchange_declare(
                exchange="jobs",
                exchange_type="direct",
                durable=True
            )
            
            channel.queue_declare(
                queue="router_jobs",
                durable=True
            )
            
            channel.queue_bind(
                queue="router_jobs",
                exchange="jobs",
                routing_key="check_interfaces"
            )
            
            channel.basic_publish(
                exchange="jobs",
                routing_key="check_interfaces",
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
            
            print(f"Sent job to RabbitMQ (size: {len(body)} bytes)")
            
            connection.close()
            return True
            
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise
        except Exception as e:
            print(f"Error publishing message: {e}")
            raise
