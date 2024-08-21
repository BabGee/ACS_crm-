import pandas as pd

# Load only the necessary columns from the CSV files, treating them as strings
contacts_df = pd.read_csv('data/Contacts.csv', usecols=['EmailID', 'Phone'], dtype=str)
subscriptions_df = pd.read_csv('data/Subscriptions.csv', usecols=['EmailID', 'SubscriptionID', 'CustomerName', 'SubscriptionNumber', 'CF.Username', 'CF.Password'], dtype=str)

# Merge the DataFrames on the 'email' column
merged_df = pd.merge(subscriptions_df, contacts_df, on='EmailID', how='left')

# Save the merged DataFrame to a new CSV
merged_df.to_csv('data/subscriptions_with_phone_numbers.csv', index=False)

print("Merged CSV created successfully.")


# Load the merged CSV file
merged_df = pd.read_csv('data/subscriptions_with_phone_numbers.csv')


#remove duplicates based on columns 'email', 'sub
deduplicated_df = merged_df.drop_duplicates(subset=['EmailID',])

# Save the deduplicated DataFrame to a new CSV file
deduplicated_df.to_csv('data/subscriptions_with_phone_numbers_deduplicated.csv', index=False)

print("Duplicates removed and CSV saved successfully.")




# TDTC-3542F0C0
# 54445443-3542F0C0