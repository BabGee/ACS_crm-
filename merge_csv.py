import pandas as pd

# Define a function to clean and normalize phone numbers
# def clean_phone_number(phone):
#     if pd.isna(phone):
#         return ''
    
#     # Convert phone to string in case it's not
#     phone = str(phone)
    
#     # Remove any non-numeric characters
#     phone = ''.join(filter(str.isdigit, phone))
    
#     # Remove the country code '254' if it exists
#     if phone.startswith('254'):
#         phone = '0' + phone[3:]
    
#     return phone

# Load only the necessary columns from the CSV files, treating them as strings
# contacts_df = pd.read_csv('data/ZOHO_SUBSCRIPTIONS/Contacts.csv',
#                            usecols=['CustomerID', 'CustomerName','EmailID', 'Phone', 'MobilePhone', 'BillingAddress', 'BillingStreet2', 'BillingCity', 'BillingState'], dtype=str)



# # Apply cleaning function to 'Phone' and 'MobilePhone' columns
# contacts_df['Phone'] = contacts_df['Phone'].apply(clean_phone_number)
# contacts_df['MobilePhone'] = contacts_df['MobilePhone'].apply(clean_phone_number)

# # 'FullBillingAddress' column by concatenating address fields
# contacts_df['FullBillingAddress'] = contacts_df['BillingAddress'].fillna('') + ', ' + \
#                                     contacts_df['BillingStreet2'].fillna('') + ', ' + \
#                                     contacts_df['BillingCity'].fillna('') + ', ' + \
#                                     contacts_df['BillingState'].fillna('')

# # Use 'Phone' if available; otherwise, use 'MobilePhone'
# contacts_df['PrimaryPhone'] = contacts_df['Phone'].where(contacts_df['Phone'] != '', contacts_df['MobilePhone'])

# # Drop unnecessary columns after processing
# contacts_df = contacts_df.drop(columns=['Phone', 'MobilePhone', 'BillingAddress', 'BillingStreet2', 
#                                         'BillingCity', 'BillingState'])

# # Save the cleaned DataFrame to a new CSV file
# contacts_df.to_csv('data/ZOHO_SUBSCRIPTIONS/Contacts_cleaned.csv', index=False)

# print("Contacts cleaned and saved successfully.")


contacts_df = pd.read_csv('data/ZOHO_SUBSCRIPTIONS/Contacts_cleaned.csv',
                           usecols=['CustomerID', 'Customer_Name','EmailID', 'PrimaryPhone', 'FullBillingAddress'], dtype=str)



subscriptions_df = pd.read_csv('data/ZOHO_SUBSCRIPTIONS/Subscriptions.csv', 
                               usecols=['CustomerID','CustomerEmail', 'SubscriptionID', 'CustomerName', 'SubscriptionNumber', 'CF.Username', 'CF.Password', 'ItemDesc'], dtype=str)

# # Merge the DataFrames on the 'CustomerID' column
merged_df = pd.merge(subscriptions_df, contacts_df, on='CustomerID', how='left')

# # Save the merged DataFrame to a new CSV
merged_df.to_csv('data/ZOHO_SUBSCRIPTIONS/ZohoContacts.csv', index=False)

print("Merged CSV created successfully.")


# # Load the merged CSV file
# merged_df = pd.read_csv('data/subscriptions_with_phone_numbers.csv')


# #remove duplicates based on columns 'email', 'sub
# deduplicated_df = merged_df.drop_duplicates(subset=['EmailID',])

# # Save the deduplicated DataFrame to a new CSV file
# deduplicated_df.to_csv('data/subscriptions_with_phone_numbers_deduplicated.csv', index=False)

# print("Duplicates removed and CSV saved successfully.")


# # Load the deduplicated CSV file
# deduplicated_df = pd.read_csv('data/subscriptions_with_phone_numbers_deduplicated.csv')



# # Apply the cleaning function to the 'Phone' column
# deduplicated_df['Phone'] = deduplicated_df['Phone'].apply(clean_phone_number)

# # Save the cleaned DataFrame back to a CSV file
# deduplicated_df.to_csv('data/subscriptions_with_phone_numbers_cleaned.csv', index=False)

# print("Phone numbers cleaned and CSV saved successfully.")


# TDTC-3542F0C0
# 54445443-3542F0C0