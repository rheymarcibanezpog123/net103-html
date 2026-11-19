import os

from netmiko import ConnectHandler


required_settings = (
    "ROUTER_IP",
    "ROUTER_USERNAME",
    "ROUTER_PASSWORD",
    "ROUTER_ENABLE_SECRET",
)
missing_settings = [
    setting for setting in required_settings if not os.environ.get(setting)
]
if missing_settings:
    raise RuntimeError(
        "Missing required environment variables: " + ", ".join(missing_settings)
    )

router_device = {
    'device_type' : 'cisco_ios_telnet',
    'ip': os.environ["ROUTER_IP"],
    'port': int(os.environ.get("ROUTER_PORT", "32770")),
    'username': os.environ["ROUTER_USERNAME"],
    'password': os.environ["ROUTER_PASSWORD"],
    'secret': os.environ["ROUTER_ENABLE_SECRET"],
}
try:
    print("Connecting to router...")
    net_connect = ConnectHandler(**router_device)


    net_connect.enable()


    commands_to_run = [
        "show version",
        "show ip interface brief",
        "show running-config",
        "show ip route"
    ]


    for cmd in commands_to_run:
        print(f"\n--- Output for: {cmd} ---")
        output = net_connect.send_command(cmd)
        print(output)


    net_connect.disconnect()
    print("\nDisconnected successfully.")
except Exception as e:
    print(f"Connection failed: {e}")