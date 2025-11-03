# router_client.py
import os
import json
import traceback
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
    SSHException
)

def get_netflow_config(ip, username, password):
    """
    เชื่อมต่อไปยัง Cisco router และดึง netflow configuration
    """
    # กำหนด device parameters
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "secret": password,
        "timeout": 30,
        "session_timeout": 60,
        "auth_timeout": 30,
        "banner_timeout": 15,
        "conn_timeout": 10
    }
    
    conn = None
    
    try:
        print(f"  Establishing SSH connection to {ip}...")
        conn = ConnectHandler(**device)
        
        print(f"  Entering enable mode...")
        conn.enable()
        
        print(f"  Executing 'show ip flow export'...")
        flow_export = conn.send_command("show ip flow export", delay_factor=2)
        
        print(f"  Executing 'show ip cache flow'...")
        cache_flow = conn.send_command("show ip cache flow", delay_factor=2)
        
        print(f"  Executing 'show ip interface brief'...")
        interfaces = conn.send_command("show ip interface brief", delay_factor=2)
        
        result = {
            "flow_export": flow_export,
            "cache_flow": cache_flow,
            "interfaces": interfaces,
            "status": "success"
        }
        
        print(f"  ✅ Successfully retrieved netflow data")
        print(f"  Output size: {len(json.dumps(result))} bytes")
        
        return result
        
    except NetmikoTimeoutException as e:
        error_msg = f"Timeout connecting to {ip}: {e}"
        print(f"  ❌ {error_msg}")
        return {
            "error": error_msg,
            "status": "timeout"
        }
        
    except NetmikoAuthenticationException as e:
        error_msg = f"Authentication failed for {ip}: {e}"
        print(f"  ❌ {error_msg}")
        return {
            "error": error_msg,
            "status": "auth_failed"
        }
        
    except SSHException as e:
        error_msg = f"SSH error connecting to {ip}: {e}"
        print(f"  ❌ {error_msg}")
        return {
            "error": error_msg,
            "status": "ssh_error"
        }
        
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(f"  ❌ {error_msg}")
        traceback.print_exc()
        return {
            "error": error_msg,
            "status": "error"
        }
        
    finally:
        if conn:
            try:
                conn.disconnect()
                print(f"  🔌 Disconnected from {ip}")
            except:
                pass

if __name__ == "__main__":
    # ทดสอบการเชื่อมต่อ
    test_ip = "192.168.1.1"
    test_user = "admin"
    test_pass = "cisco"
    
    result = get_netflow_config(test_ip, test_user, test_pass)
    print(json.dumps(result, indent=2))
