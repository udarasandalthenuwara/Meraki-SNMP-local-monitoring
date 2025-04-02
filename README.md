# Meraki Device Monitor

A lightweight Flask web application that monitors the status (Online/Offline) and hostnames of Cisco Meraki devices using SNMP (via `easysnmp`). The application fetches device data from a configurable `devices.txt` file, polls the devices periodically, and displays the results in a scrollable HTML table with real-time updates.

## Features
- Monitors Meraki device status using SNMP (`sysUpTime` OID) and retrieves hostnames (`sysName` OID).
- Displays results in a clean, scrollable table with IP, Hostname, and Status columns.
- Real-time updates every 10 seconds (configurable).
- Detailed error logging for troubleshooting.
- Responsive web UI with color-coded statuses (green for Online, red for Offline).

## Prerequisites
- Python 3.6+
- A Meraki network with SNMP enabled and devices configured to respond to SNMP queries.
- Network access to the devices (UDP port 161 open).

## Installation

## 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Meraki-Device-Monitor.git
cd Meraki-Device-Monitor
```
## 2.Set Up a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
# On Windows: 
```bash
.venv\Scripts\activate
```

## 3.Install Dependencies
```bash
pip install flask easysnmp
```


## 4.Configure Devices
Create a devices.txt file in the project root with one Meraki device IP per line:
192.168.128.10
192.168.128.11
192.168.128.12

## 5.Update Configuration (Optional)
Edit app.py to set your SNMP community string (default: "meraki"):
COMMUNITY_STRING = "your_community_string"
Adjust POLL_INTERVAL, TIMEOUT, or RETRIES if needed.

----------------------------------------------------------------------

## Usage
Run the Application
python app.py

## Access the Web UI
Open a browser and go to http://localhost:5100.
The table will display the IP, hostname, and status of each device, updating every 10 seconds.

![image](https://github.com/user-attachments/assets/eaaaf76f-20bb-4c8b-adc4-254c8010e011)

