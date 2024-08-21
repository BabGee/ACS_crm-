import os

import pandas as pd

from netmiko import ConnectHandler
import logging
logging.basicConfig(filename='netmiko_log.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")


def extract_ontid_csv():
    """Extracts all ONT IDs from the CSV file."""
    olt_csv = pd.read_csv('data/nrb_west_p4.csv', usecols=['ont_id'])
    return olt_csv['ont_id'].tolist()

def provision_ont():
    """Provisions each ONT on the OLT."""
    device = {
        'host': os.getenv('OLT_HOST'),
        'device_type': 'huawei_olt', 
        'username': os.getenv('OLT_USERNAME'),
        'password': os.getenv('OLT_PASSWORD'),
        'session_log': 'netmiko_session.log',
    }
 
    logger.info(f"Connecting to OLT at {device['host']} with username {device['username']}")
    
    try:
        with ConnectHandler(**device) as conn:
            logger.info("BEGIN Execution")
            find_prompt = conn.find_prompt()
            if not '#' in find_prompt:
                conn.enable()
                logger.info("Connection established")
                conn.send_command_timing('config', read_timeout=0)   
                conn.send_command_timing("interface gpon 0/1", read_timeout=0)
                
                # Extract all ONT IDs from the CSV
                ont_ids = extract_ontid_csv()
                
                for ont_id in ont_ids:
                    logger.info(f"Configuring ONT ID: {ont_id}")
                    config_commands = [
                        f"ont ipconfig 4 {ont_id} dhcp vlan 91 priority 2", 
                        f"ont tr069-server-config 4 {ont_id} profile-id 2"
                    ]
                    conn.send_config_set(config_commands)
                    conn.send_command_timing('config', read_timeout=0)
                    service_port_cmd = (f"service-port vlan 91 gpon 0/1/4 ont {ont_id}"
                                        "gemport 2 multi-service user-vlan 91"
                                        "tag-transform translate inbound traffic-table index 8"
                                        "outbound traffic-table index 8")
                    conn.send_command_timing(service_port_cmd, read_timeout=0)
                    logger.info(f"ONT ID {ont_id} configured successfully.")
                
                logger.info("All ONTs provisioned successfully.")
            else:
                logger.warning("Connection issue detected.")

    except Exception as e:
        logger.error(f"Error during provisioning: {e}")

if __name__ == "__main__":
    try:
        provision_ont()
    except Exception as e:
        logger.error(f"Provisioning failed: {e}")