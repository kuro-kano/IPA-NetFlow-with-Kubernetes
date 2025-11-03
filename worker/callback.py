# callback.py
import traceback
from bson import json_util
from router_client import get_netflow_config
from database import save_netflow_status


def callback(ch, method, props, body):
    """Process message from RabbitMQ"""
    try:
        job = json_util.loads(body.decode())

        router_ip = job.get("ip")
        router_username = job.get("username")
        router_password = job.get("password")
        router_hostname = job.get("hostname", router_ip)

        if not all([router_ip, router_username, router_password]):
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        output = get_netflow_config(router_ip, router_username, router_password)
        save_netflow_status(router_ip, router_hostname, output)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except KeyError as e:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Exception as e:
        traceback.print_exc()

        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
