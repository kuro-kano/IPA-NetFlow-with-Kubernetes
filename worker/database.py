from pymongo import MongoClient
from datetime import datetime, UTC
import os


def save_netflow_status(router_ip, netflow_data):

    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["netflow_status"]

    data = {
        "router_ip": router_ip,
        "timestamp": datetime.now(UTC),
        "netflow_data": netflow_data,
    }
    collection.insert_one(data)
    client.close()
