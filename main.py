from flask import Flask, render_template, jsonify
from easysnmp import Session
import threading
import time
import logging

app = Flask(__name__)

# Configuration
DEVICE_FILE = "devices.txt"
COMMUNITY_STRING = "meraki"  # Replace with your SNMP community string
POLL_INTERVAL = 10  # Seconds between polls
TIMEOUT = 5  # Timeout in seconds
RETRIES = 3  # Number of retries

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_devices(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Failed to load devices from {file_path}: {e}")
        return []

def get_device_info(ip):
    try:
        # Create an SNMP session
        session = Session(hostname=ip, community=COMMUNITY_STRING, version=2, timeout=TIMEOUT, retries=RETRIES)

        # Poll sysUpTime for status
        uptime = session.get('1.3.6.1.2.1.1.3.0')  # sysUpTime OID
        status = "Online" if uptime.value != "NOSUCHOBJECT" else "Offline"

        # Poll sysName for hostname
        hostname_var = session.get('1.3.6.1.2.1.1.5.0')  # sysName OID
        hostname = hostname_var.value if hostname_var.value != "NOSUCHOBJECT" else "Unknown"

        if status == "Offline":
            logger.warning(f"Device {ip} offline: sysUpTime not available")
        elif hostname == "Unknown":
            logger.warning(f"Hostname not available for {ip}")

        return {"ip": ip, "hostname": hostname, "status": status}
    except Exception as e:
        logger.error(f"Exception for {ip}: {str(e)}")
        return {"ip": ip, "hostname": "Unknown", "status": f"Offline (Error: {str(e)})"}

# Load initial devices
DEVICE_IPS = load_devices(DEVICE_FILE)
device_statuses = {ip: {"hostname": "Unknown", "status": "Checking"} for ip in DEVICE_IPS}

# Background thread to update statuses
def update_statuses():
    global device_statuses
    while True:
        for ip in DEVICE_IPS:
            device_info = get_device_info(ip)
            device_statuses[ip] = {"hostname": device_info["hostname"], "status": device_info["status"]}
        time.sleep(POLL_INTERVAL)

# Start the background thread
thread = threading.Thread(target=update_statuses, daemon=True)
thread.start()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html', devices=device_statuses)

# API endpoint to fetch updated statuses
@app.route('/status')
def get_status():
    return jsonify(device_statuses)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)