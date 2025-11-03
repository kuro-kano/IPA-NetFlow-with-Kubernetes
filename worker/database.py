# database.py
import os
from pymongo import MongoClient
from datetime import datetime, UTC


def save_netflow_status(router_ip, router_hostname, netflow_data):
    """Save netflow status to MongoDB"""
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")

    if not MONGO_URI or not DB_NAME:
        raise ValueError("MONGO_URI and DB_NAME must be set")

    client = None

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()

        db = client[DB_NAME]
        collection = db["netflow_status"]

        data = {
            "router_ip": router_ip,
            "router_hostname": router_hostname,
            "timestamp": datetime.now(UTC),
            "netflow_data": netflow_data,
            "status": "success",
        }

        result = collection.insert_one(data)

        return result.inserted_id

    except Exception as e:
        print(f"Database error: {e}")
        raise

    finally:
        if client:
            client.close()


def get_router_credentials(router_ip):
    """Get router credentials from database"""
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")

    client = None

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        routers = db["routers"]

        router = routers.find_one({"ip": router_ip})
        return router

    finally:
        if client:
            client.close()
