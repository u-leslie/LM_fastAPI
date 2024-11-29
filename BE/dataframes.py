import pandas as pd
import requests
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL') 

drivers_api_url = 'http://127.0.0.1:8000/drivers/drivers'
shipments_api_url = 'http://127.0.0.1:8000/shipments/shipments'

try:
    print("Fetching data from Drivers API...")
    drivers_api_response = requests.get(drivers_api_url)
    drivers_api_response.raise_for_status() 
    drivers_api_data = drivers_api_response.json()

    drivers_df = pd.DataFrame(drivers_api_data)
    print("Drivers DataFrame loaded successfully!")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Drivers API: {e}")
    drivers_df = pd.DataFrame()  

try:
    print("Fetching data from Shipments API...")
    shipments_api_response = requests.get(shipments_api_url)
    shipments_api_response.raise_for_status() 
    shipments_api_data = shipments_api_response.json()

    shipments_df = pd.DataFrame(shipments_api_data)
    print("Shipments DataFrame loaded successfully!")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Shipments API: {e}")
    shipments_df = pd.DataFrame()  

if not drivers_df.empty:
    print("\nDescription of the Drivers Dataset:")
    print(drivers_df.describe())  
    print(drivers_df.info())  
else:
    print("\nNo data in Drivers DataFrame.")

if not shipments_df.empty:
    print("\nDescription of the Shipments Dataset:")
    print(shipments_df.describe())  
    print(shipments_df.info())  
else:
    print("\nNo data in Shipments DataFrame.")


print("\nHandling missing data:")
drivers_df.fillna('Unknown', inplace=True)
shipments_df.fillna('Unknown', inplace=True)


print("\nMissing Data After Filling:")
print(drivers_df.isnull().sum())
print(shipments_df.isnull().sum())

if 'is_available' in drivers_df.columns:
    drivers_df['is_available'] = drivers_df['is_available'].astype(bool)

if 'status' in shipments_df.columns:
    shipments_df = pd.get_dummies(shipments_df, columns=['status'], drop_first=True)

if 'phone_number' in drivers_df.columns:
    drivers_df['phone_number_length'] = drivers_df['phone_number'].apply(lambda x: len(str(x)))

merged_df = pd.merge(drivers_df, shipments_df, left_on='id', right_on='driver_id', how='inner', suffixes=('_driver', '_shipment'))
merged_df.to_csv('merged_data.csv', index=False)

print("\nFinal Merged DataFrame with New Features:")
print(merged_df.head())
