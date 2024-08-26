import os

import pandas as pd

from netmiko import ConnectHandler

import logging
logging.basicConfig(filename='netmiko_logs/netmiko_log.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

from dotenv import load_dotenv


load_dotenv()

def extract_ontid_csv():
    """Extracts all ONT IDs from the CSV file."""
    olt_csv = pd.read_csv('data/syk_olt_p_11.csv', usecols=['ont_id'])
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
                # conn.enable()
                # logger.info("Connection established")
                # conn.send_command_timing('config', read_timeout=5)   
                # conn.send_command_timing("interface gpon 0/13", read_timeout=5)
                
                # Extract all ONT IDs from the CSV
                ont_ids = extract_ontid_csv()
                
                
                for ont_id in ont_ids:
                    logger.info(f"Migrating ONT ID: {ont_id}")
                    conn.enable()
                    logger.info("Connection established")
                    conn.send_command_timing('config', read_timeout=5)   
                    conn.send_command_timing("interface gpon 0/13", read_timeout=5)                    
                    config_commands = [
                        f"ont ipconfig 11 {ont_id} dhcp vlan 91 priority 2", 
                        f"ont tr069-server-config 11 {ont_id} profile-id 2"
                    ]
                    conn.enable()
                    conn.send_config_set(config_commands)
                    conn.send_command_timing('config', read_timeout=10)
                    service_port_cmd = f"service-port vlan 91 gpon 0/13/11 ont {ont_id} gemport 2 multi-service user-vlan 91 tag-transform translate inbound traffic-table index 8 outbound traffic-table index 8"
                    conn.send_command_timing(service_port_cmd, read_timeout=10)
                    logger.info(f"ONT ID {ont_id} configured successfully.")
                
                logger.info("All ONTs Migrated successfully.")
            else:
                logger.warning("Connection issue detected.")

    except Exception as e:
        logger.error(f"Error during Migration: {e}")

if __name__ == "__main__":
    try:
        provision_ont()
    except Exception as e:
        logger.error(f"Migration failed: {e}")