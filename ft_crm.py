import pandas as pd
import requests
import os


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
                "Name": record['name'],
                "Telephone": record['phone'],  
                "Location": record['sub_id'],  
                "Tag": record['olt'], 
                "Id":record['sub_number'],  
                "Cust1": record['username'], 
                "Cust2": record['password'],  
                #"Cust7": record['address'], 
                "Cust8": record['email'],                 
            },
            "Parameters": [],
            "Creator": "syk_script",  
            "AppId": "REST_API",  
            "CreatorPassword": "SYK"  
        }
        
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Success: {record['username']}")
        else:
            print(f"Failed: {record['username']} with status code {response.status_code}")

def check_device(sn):
    url = os.getenv('CHECKDV_API')
    headers = {'Content-Type': 'application/json'}

    payload = {
        "Device": {
            "Sn": sn,
        },
        "Creator": "rest_api",
        "AppId": "api",
        "CreatorPassword": ""
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Success: {record['username']}")
    else:
        print(f"Failed: {record['username']} with status code {response.status_code}")

olt_csv = pd.read_csv('data/syk_olt.csv', usecols=['SN','OLT', 'Username', 'Password'], dtype=str)
subscriptions_df = pd.read_csv('data/subscriptions_with_phone_numbers_deduplicated.csv', dtype=str)

# Iterate over each row in olt_csv.
for index, row in olt_csv.iterrows():
    username = row['Username']
    serial_number = row['SN']

    check_device(serial_number)

    # Check if the username exists in subscriptions_with_phone_numbers_deduplicated.csv
    matching_row = subscriptions_df[subscriptions_df['Username'] == username]
    
    if not matching_row.empty:
        # Extract the email, phone, and name fields
        email = matching_row.iloc[0]['EmailID']
        phone = matching_row.iloc[0]['Phone']
        name = matching_row.iloc[0]['CustomerName']
        sub_id = matching_row.iloc[0]['SubscriptionID']
        sub_no = matching_row.iloc[0]['SubscriptionNumber']
        username_confirm = matching_row.iloc[0]['Username']

        if username == username_confirm:
            # Prepare the data to be sent to the external API
            data = {
                'serial_number': row['SN'],
                'olt': row['OLT'],
                'username': username,
                'password': row['password'],
                'email': email,
                'phone': phone,
                'name': name,
                'sub_id': sub_id,
                'sub_number': sub_no,
            }

            api_call(data)



