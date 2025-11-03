"""Worker that starts the consumer to process jobs from RabbitMQ."""

import os

from consumer import consume

consume(os.getenv("RABBITMQ_HOST", "rabbitmq-svc"))
