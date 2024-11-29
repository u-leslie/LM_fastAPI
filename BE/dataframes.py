import pandas as pd
import requests

try:
    print("Fetching data from drivers API...")
    drivers_api = requests.get('http://127.0.0.1:8000/drivers/drivers')
    drivers_api.raise_for_status()
    drivers_api_data = drivers_api.json()

    print("Fetching data from shipments API...")
    shipments_api = requests.get('http://127.0.0.1:8000/shipments/shipments')
    shipments_api.raise_for_status()
    shipments_api_data = shipments_api.json()

    print("Inspecting Drivers API Data:")
    print(drivers_api_data[:5])  

    print("Inspecting Shipments API Data:")
    print(shipments_api_data[:5])  

    drivers_df = pd.DataFrame(drivers_api_data if isinstance(drivers_api_data, list) else drivers_api_data.get('drivers', []))
    shipments_df = pd.DataFrame(shipments_api_data if isinstance(shipments_api_data, list) else shipments_api_data.get('shipments', []))

    print("Drivers DataFrame columns:", drivers_df.columns)
    print("Shipments DataFrame columns:", shipments_df.columns)

    
    print("Merging DataFrames...")
    merged_df = pd.merge(
        drivers_df, shipments_df, left_on='id', right_on='driver_id', how='inner', suffixes=('_driver', '_shipment')
    )

    print("Feature Engineering...")
    merged_df['is_active'] = merged_df['driver_id'].apply(lambda x: 1 if pd.notnull(x) else 0)

    merged_df.ffill(inplace=True)
    merged_df.bfill(inplace=True)

    print("Final DataFrame:")
    print(merged_df.head())  

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")

except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
