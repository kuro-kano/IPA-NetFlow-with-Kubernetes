# database.py
import os
from pymongo import MongoClient

def get_router_info():
    """ดึงข้อมูล Router ทั้งหมดจาก MongoDB"""
    mongo_uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME")
    
    if not mongo_uri or not db_name:
        raise ValueError("MONGO_URI และ DB_NAME ต้องถูกกำหนดใน environment variables")
    
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        routers = db["routers"]
        
        # ดึงข้อมูล router ทั้งหมดที่ active
        router_data = list(routers.find({"status": {"$ne": "inactive"}}))
        
        print(f"Found {len(router_data)} routers in database")
        return router_data
    
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    routers = get_router_info()
    for router in routers:
        print(router)