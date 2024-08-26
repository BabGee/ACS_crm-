import pandas as pd
import requests
import os


def FT_update_userinfo(data):
    url = os.getenv('USERINFO_API')
    headers = {'Content-Type': 'application/json'}

    for record in data:
        payload = {
            "Device": {
                "Sn": record['serial_number'],
            },
            "UserInfo": {
                "LoginName": record['plan_name'],
                "Name": record['name'],
                "Telephone": record['phone'],  
                "Location": record['sub_id'],  
                "UserTag": record['olt'], 
                "id":record['sub_number'],  
                "Cust1": record['username'], 
                "Cust2": record['password'], 
                "Cust7": record['billing_address'], 
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
olt_csv = pd.read_csv('data/syk_olt_p_11.csv', usecols=['SN', 'OLT', 'Username', 'Password'], dtype=str) # use exported OLT CSV
subscriptions_df = pd.read_csv('data/ZOHO_SUBSCRIPTIONS/ZohoContacts.csv', dtype=str)

# Iterate over each row in olt_csv.
for index, row in olt_csv.iterrows():
    username = row['Username']
    serial_number = row['SN']

    if "HWTC" in serial_number:
        serial_number = serial_number.replace("HWTC", "48575443")
    elif "TDTC" in serial_number:
        serial_number = serial_number.replace("TDTC", "54445443")

    # Check if the username exists in ZohoContacts.csv
    matching_rows = subscriptions_df[subscriptions_df['CF.Username'] == username]
    
    if not matching_rows.empty:
        records = []
        
        # Iterate over all matching rows to prepare data
        for _, matching_row in matching_rows.iterrows():
            email = matching_row['EmailID']
            phone = matching_row['PrimaryPhone']
            name = matching_row['CustomerName']
            sub_id = matching_row['SubscriptionID']
            sub_no = matching_row['SubscriptionNumber']
            plan_name = matching_row['ItemDesc']
            billing_address = matching_row['FullBillingAddress']

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
                'plan_name': plan_name,
                'billing_address': billing_address
            })
        print(f"RECORD>> {records}")    

        FT_update_userinfo(records)
    else:
        print(f"No matching subscriptions found for username: {username}") 



