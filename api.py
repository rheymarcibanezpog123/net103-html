
import os

from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    error = None

    if request.method == "POST":
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
            error = (
                "Missing required environment variables: "
                + ", ".join(missing_settings)
            )
            return render_template(
                "index.html",
                results=results,
                error=error
            )

        commands_to_run = [
            "show version",
            "show ip interface brief",
            "show running-config"
        ]

        net_connect = None

        try:
            router_device = {
                'device_type': 'cisco_ios_telnet',
                'ip': os.environ["ROUTER_IP"],
                'port': int(os.environ.get("ROUTER_PORT", "32770")),
                'username': os.environ["ROUTER_USERNAME"],
                'password': os.environ["ROUTER_PASSWORD"],
                'secret': os.environ["ROUTER_ENABLE_SECRET"],
                'fast_cli': False,
                'global_delay_factor': 2,
            }
            net_connect = ConnectHandler(**router_device)

            net_connect.enable()

            net_connect.send_command_timing("terminal length 0")

            for cmd in commands_to_run:
                output = net_connect.send_command_timing(
                    cmd,
                    read_timeout=60
                )
                results[cmd] = output

        except Exception as e:
            error = f"Connection failed: {e}"

        finally:
            if net_connect:
                net_connect.disconnect()

    return render_template(
        "index.html",
        results=results,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
