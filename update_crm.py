import pandas as pd

import requests

import os
from dotenv import load_dotenv

load_dotenv()

def read_csv(file_path):
    data = pd.read_csv(file_path)
    return data[['SN','OLT', 'Username', 'Password']]

def read_xlsx(file_path):
    data = pd.read_excel(file_path)
    return data[['username','Customer', 'CustomerID', 'accountNumber']]

def extract_details(csv_file, xlsx_file):
    # Read CSV and Excel files
    csv_data = read_csv(csv_file)
    xlsx_data = read_xlsx(xlsx_file)
    
    # Dictionary to store extracted details
    extracted_data = []

    # Iterate through CSV data
    for index, row in csv_data.iterrows():
        serial_number = row['SN'].replace("HWTC", "48575443")
        username = row['Username']
        password = row['Password']
        olt = row['OLT']
        
        # Find matching row in Excel data
        customer_details = xlsx_data[xlsx_data['username'] == username]
        
        if not customer_details.empty:
            customer_name = customer_details['Customer'].values[0]
            customer_id = customer_details['CustomerID'].values[0].split('_')[-1]
            account_no = customer_details['accountNumber'].values[0]

            # Store extracted details
            extracted_data.append({
                'serial_number': serial_number,
                'username': username,
                'password': password,
                'olt':olt,
                'customer_name': customer_name,
                'customer_id': customer_id,
                'account_no': account_no
            })
    print(f"Extracted Data: {extract_details}")
    return extracted_data

def api_call(data):
    url = os.getenv('USERINFO_API')
    headers = {'Content-Type': 'application/json'}

    for record in data:
        payload = {
            "Device": {
                "Sn": record['serial_number'],
            },
            "UserInfo": {
                "LoginName": record['username'],
                "FullName": record['customer_name'],
                #"Telephone": record['phone'],  
                "UserId": record['customer_id'],
                #"Location": record['location'],  
                "UserTag": record['olt'],   
                "Cust1": record['username'], 
                "Cust2": record['password']  
            },
            "Parameters": [
                    # {
                    # "Name": "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.2.WANPPPConnection.1.Username",
                    # "Value": record['username'],
                    # },
                    # {
                    # "Name": "InternetGatewayDevice.WANDevice.1.WANConnectionDevice.2.WANPPPConnection.1.Password",
                    # "Value": record['password'],
                    # }
            ],
            "Creator": "syk_script",  
            "AppId": "REST_API",  
            "CreatorPassword": "SYK"  
        }
        
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Success: {record['username']}")
        else:
            print(f"Failed: {record['username']} with status code {response.status_code}")


def main():
    csv_file = os.getenv('PATH_TO_CSV_FILE')
    xlsx_file = os.getenv('PATH_TO_XLSX_FILE')
    
    extracted_data = extract_details(csv_file, xlsx_file)
    
    # Perform API calls with the extracted data
    api_call(extracted_data)

if __name__ == '__main__':
    main()
