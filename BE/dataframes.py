# from fastapi import FastAPI, HTTPException
# import pandas as pd
# import requests

# app = FastAPI()

# # API endpoint to fetch and analyze data
# @app.get("/analytics")
# def get_analytics():
#     try:
#         # Fetch drivers data
#         drivers_api = requests.get('http://127.0.0.1:8000/drivers/drivers')
#         drivers_api.raise_for_status()  # Raises an HTTPError for bad responses
#         drivers_api_data = drivers_api.json()

#         # Fetch shipments data
#         shipments_api = requests.get('http://127.0.0.1:8000/shipments/shipments')
#         shipments_api.raise_for_status()
#         shipments_api_data = shipments_api.json()

#         # Create DataFrames from the fetched data
#         drivers_df = pd.DataFrame(drivers_api_data if isinstance(drivers_api_data, list) else drivers_api_data.get('drivers', []))
#         shipments_df = pd.DataFrame(shipments_api_data if isinstance(shipments_api_data, list) else shipments_api_data.get('shipments', []))
#         print(drivers_df)
#         print(shipments_df)

#         # Inner Join on 'user_id' from drivers and 'id' from shipments
#         merged_df = pd.merge(
#             drivers_df, shipments_df, left_on='user_id', right_on='id', how='inner', suffixes=('_driver', '_shipment')
#         )
#         print("Merged data"+merged_df)

#         # Feature Engineering
#         # 1. Email Length: Feature for the length of the user's email
#         merged_df['email_length'] = merged_df['email'].apply(len)

#         # 2. User-Post Time Difference: Assuming 'created_at_driver' and 'created_at_shipment' are timestamps
#         merged_df['user_post_difference'] = pd.to_datetime(merged_df['created_at_shipment']) - pd.to_datetime(merged_df['created_at_driver'])
#         merged_df['user_post_difference'] = merged_df['user_post_difference'].dt.days  # Convert to days

#         # 3. Is Active: Mark drivers with at least one shipment as active
#         merged_df['is_active'] = merged_df['id_shipment'].apply(lambda x: 1 if pd.notnull(x) else 0)

#         # Handle missing values using ffill and bfill
#         merged_df.ffill(inplace=True)  # Forward fill
#         merged_df.bfill(inplace=True)  # Backward fill

#         # Return the result as a dictionary or list of dictionaries for FastAPI response
#         return merged_df.to_dict(orient='records')  # Converts DataFrame to list of dicts
    
#     except requests.exceptions.RequestException as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching data from API: {e}")
    
#     except Exception as ex:
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {ex}")

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
    print(drivers_api_data[:5])  # Print the first 5 records to inspect the data

    print("Inspecting Shipments API Data:")
    print(shipments_api_data[:5])  # Print the first 5 records to inspect the data

    # Create DataFrames
    drivers_df = pd.DataFrame(drivers_api_data if isinstance(drivers_api_data, list) else drivers_api_data.get('drivers', []))
    shipments_df = pd.DataFrame(shipments_api_data if isinstance(shipments_api_data, list) else shipments_api_data.get('shipments', []))

    print("Drivers DataFrame columns:", drivers_df.columns)
    print("Shipments DataFrame columns:", shipments_df.columns)

    # Merge DataFrames on 'id' from drivers and 'driver_id' from shipments
    print("Merging DataFrames...")
    merged_df = pd.merge(
        drivers_df, shipments_df, left_on='id', right_on='driver_id', how='inner', suffixes=('_driver', '_shipment')
    )

    # Feature Engineering
    print("Feature Engineering...")
    # 1. Email Length: Skipping since 'email' doesn't exist.
    # 2. User-Post Time Difference: Skipping timestamp features due to missing timestamps.
    # 3. Is Active: Marking shipments where driver is assigned
    merged_df['is_active'] = merged_df['driver_id'].apply(lambda x: 1 if pd.notnull(x) else 0)

    # Handle missing values
    merged_df.ffill(inplace=True)
    merged_df.bfill(inplace=True)

    print("Final DataFrame:")
    print(merged_df.head())  # Output the first few rows of the DataFrame

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")

except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
