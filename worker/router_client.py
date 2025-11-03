# router_client.py
import os
import json
import traceback
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
    SSHException,
)


def get_netflow_config(ip, username, password):
    """Connect to router and retrieve netflow config"""
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
        "conn_timeout": 10,
    }

    conn = None

    try:
        conn = ConnectHandler(**device)

        print(f"  Entering enable mode...")
        conn.enable()
        flow_export = conn.send_command("show ip flow export", delay_factor=2)
        cache_flow = conn.send_command("show ip cache flow", delay_factor=2)
        interfaces = conn.send_command("show ip interface brief", delay_factor=2)

        result = {
            "flow_export": flow_export,
            "cache_flow": cache_flow,
            "interfaces": interfaces,
            "status": "success",
        }

        return result

    except NetmikoTimeoutException as e:
        error_msg = f"Timeout connecting to {ip}: {e}"
        print(f"  {error_msg}")
        return {"error": error_msg, "status": "timeout"}

    except NetmikoAuthenticationException as e:
        error_msg = f"Authentication failed for {ip}: {e}"
        print(f"  {error_msg}")
        return {"error": error_msg, "status": "auth_failed"}

    except SSHException as e:
        error_msg = f"SSH error connecting to {ip}: {e}"
        print(f"  {error_msg}")
        return {"error": error_msg, "status": "ssh_error"}

    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(f"  {error_msg}")
        traceback.print_exc()
        return {"error": error_msg, "status": "error"}

    finally:
        if conn:
            conn.disconnect()
