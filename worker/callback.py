# callback.py
import traceback
from bson import json_util
from router_client import get_netflow_config
from database import save_netflow_status

def callback(ch, method, props, body):
    """
    Callback function ที่จะถูกเรียกเมื่อได้รับ message จาก RabbitMQ
    """
    try:
        # แปลง JSON bytes กลับเป็น dictionary
        job = json_util.loads(body.decode())
        
        # ดึงข้อมูลจาก job
        router_ip = job.get("ip")
        router_username = job.get("username")
        router_password = job.get("password")
        router_hostname = job.get("hostname", router_ip)
        
        if not all([router_ip, router_username, router_password]):
            print(f"❌ Missing required fields in job: {job}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        print(f"\n{'='*60}")
        print(f"📥 Received job for router: {router_hostname} ({router_ip})")
        print(f"{'='*60}")
        
        # เชื่อมต่อ router และดึง netflow config
        print(f"🔌 Connecting to {router_ip}...")
        output = get_netflow_config(router_ip, router_username, router_password)
        
        # บันทึกลง database
        print(f"💾 Saving netflow status to database...")
        save_netflow_status(router_ip, router_hostname, output)
        
        print(f"✅ Successfully processed job for {router_hostname}")
        print(f"{'='*60}\n")
        
        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except KeyError as e:
        print(f"❌ Missing key in job data: {e}")
        print(f"Job content: {body.decode()}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
    except Exception as e:
        print(f"❌ Error processing job: {e}")
        print(f"Traceback:")
        traceback.print_exc()
        
        # ไม่ requeue เพราะอาจจะ error ซ้ำ
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
