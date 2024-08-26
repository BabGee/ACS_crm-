import pandas as pd
import requests
import os


# def check_device(sn):
#     url = os.getenv('CHECKDV_API')
#     headers = {'Content-Type': 'application/json'}

#     payload = {
#         "Device": {
#             "Sn": sn,
#         },
#         "Creator": "rest_api",
#         "AppId": "api",
#         "CreatorPassword": ""
#     }
    
#     response = requests.post(url, headers=headers, json=payload)
#     if response.status_code == 200:
#         print(f"Success: {record['username']}")
#     else:
#         print(f"Failed: {record['username']} with status code {response.status_code}")

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
                "id":record['sub_number'],  
                "Cust1": record['username'], 
                "Cust2": record['password'],  
                #"Cust7": record['address'], 
                "Cust8": record['email'], 
                'Cust9': f"https://billing.zoho.com/app/809359528#/subscriptions/{record['sub_id']}"           
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


# Load the data from CSV files
olt_csv = pd.read_csv('data/syk_olt_p_11.csv', usecols=['SN', 'OLT', 'Username', 'Password'], dtype=str)
subscriptions_df = pd.read_csv('data/subscriptions_with_phone_numbers_cleaned.csv', dtype=str)

# Iterate over each row in olt_csv.
for index, row in olt_csv.iterrows():
    username = row['Username']
    serial_number = row['SN'].replace("HWTC", "48575443")

    # Check if the username exists in subscriptions_with_phone_numbers_deduplicated.csv
    matching_rows = subscriptions_df[subscriptions_df['CF.Username'] == username]
    
    if not matching_rows.empty:
        records = []
        
        # Iterate over all matching rows to prepare data
        for _, matching_row in matching_rows.iterrows():
            email = matching_row['EmailID']
            phone = matching_row['Phone']
            name = matching_row['CustomerName']
            sub_id = matching_row['SubscriptionID']
            sub_no = matching_row['SubscriptionNumber']

            records.append({
                'serial_number': serial_number,
                'olt': row['OLT'],
                'username': username,
                'password': row['Password'],
                'email': email,
                'phone': phone,
                'name': name,
                'sub_id': sub_id,
                'sub_number': sub_no,
            })
        print(f"RECORD>> {records}")    

        # Send the collected records to the API
        api_call(records)
    else:
        print(f"No matching subscriptions found for username: {username}") 



