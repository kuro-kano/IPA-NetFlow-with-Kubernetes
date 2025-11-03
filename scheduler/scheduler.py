# scheduler.py
import os
import time
from bson import json_util
from producer import produce
from database import get_router_info

def scheduler():
    """Main scheduler loop to send jobs to workers"""
    INTERVAL = float(os.getenv("SCHEDULER_INTERVAL", "60"))
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq-svc")
    
    print(f"Scheduler started with interval: {INTERVAL} seconds")
    print(f"RabbitMQ host: {RABBITMQ_HOST}")
    print(f"MongoDB URI: {os.getenv('MONGO_URI', 'Not set')}")
    print(f"Database name: {os.getenv('DB_NAME', 'Not set')}")
    
    next_run = time.monotonic()
    count = 0
    
    print("Waiting for services to be ready...")
    time.sleep(10)
    
    while True:
        try:
            now = time.time()
            now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            ms = int((now % 1) * 1000)
            now_str_with_ms = f"{now_str}.{ms:03d}"
            
            print(f"\n[{now_str_with_ms}] === Run #{count} ===")
            
            router_data = get_router_info()
            
            if not router_data:
                print("No routers found in database")
            else:
                for idx, data in enumerate(router_data):
                    try:
                        body_bytes = json_util.dumps(data).encode("utf-8")
                        produce(RABBITMQ_HOST, body_bytes)
                        
                        router_info = data.get('hostname', data.get('ip', 'unknown'))
                        print(f"  [{idx+1}/{len(router_data)}] Sent job for router: {router_info}")
                        
                    except Exception as e:
                        print(f"  Error processing router {idx+1}: {e}")
                        continue
                
                print(f"Successfully sent {len(router_data)} jobs to queue")
            
        except Exception as e:
            print(f"ERROR in scheduler loop: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)
            continue
        
        count += 1
        next_run += INTERVAL
        
        sleep_time = max(0.0, next_run - time.monotonic())
        
        if sleep_time > 0:
            print(f"Sleeping for {sleep_time:.2f} seconds until next run...")
            time.sleep(sleep_time)
