from netmiko import ConnectHandler
import ntc_templates
import os
import json


def get_netflow_config(ip, username, password):

    os.environ["NET_TEXTFSM"] = os.path.join(
        os.path.dirname(ntc_templates.__file__), "templates"
    )

    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "secret": password,  # ใช้ password เดียวกันสำหรับ enable
    }

    with ConnectHandler(**device) as conn:
        conn.enable()
        # Get netflow configuration
        result = conn.send_command("show ip flow export", use_textfsm=False)
        conn.disconnect()

    print(json.dumps({"output": result}, indent=2))
    return {"output": result}


if __name__ == "__main__":
    get_netflow_config()
