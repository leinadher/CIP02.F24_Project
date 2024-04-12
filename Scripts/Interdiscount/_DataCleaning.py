# 24.03.2024

import re
import pandas as pd
import warnings
from _DeliveryPickupTime import convert_delivery_time, convert_pickup_time

# To prevent FutureWarnings from displaying
warnings.simplefilter(action='ignore', category=FutureWarning)

df_interdiscount = pd.read_csv("./interdiscount_scraped.csv")



# ID
df_interdiscount['id'] = pd.to_numeric(df_interdiscount['id'], errors='coerce').astype(pd.Int64Dtype())
df_interdiscount['id'] = df_interdiscount['id'].astype(str)

# PRICE
df_interdiscount['price'].fillna(df_interdiscount['price'].mean(), inplace=True)

# RATING
df_interdiscount['rating'] = df_interdiscount['rating'].astype(float)

# DELIVERY TIME
df_interdiscount['delivery_time'] = [convert_delivery_time(i) for i in df_interdiscount['delivery_time']]
df_interdiscount['delivery_time'] = df_interdiscount['delivery_time'].astype(pd.Int64Dtype())

# PICKUP TIME
df_interdiscount['pickup_time'] = [convert_pickup_time(i) for i in df_interdiscount['pickup_time']]
df_interdiscount['delivery_time'] = df_interdiscount['pickup_time'].astype(pd.Int64Dtype())


# Fixing brand = "NOTHING"
# Function to extract the 'model'
def extract_model(url):
    match = re.search(r'nothing-phone-(\d+)([a-zA-Z]?)', url)
    if match:
        number = match.group(1)
        letter = match.group(2)
        return f"Phone {number}{letter}"
    else:
        return None

# Extract model information from URLs for rows where 'brand' is "NOTHING"
nothing_rows = df_interdiscount[df_interdiscount['brand'] == 'NOTHING']
df_interdiscount.loc[nothing_rows.index, 'model'] = nothing_rows['webpage'].apply(extract_model)

# Function to correct 'network'
def extract_5g(network):
    match = re.search(r'\((\d+G)', network)
    if match:
        return match.group(1)
    else:
        return None

# Extract 5G information from 'network' column for rows where 'brand' is "NOTHING"
nothing_rows = df_interdiscount[df_interdiscount['brand'] == 'NOTHING']
df_interdiscount.loc[nothing_rows.index, 'network'] = nothing_rows['network'].apply(extract_5g)


# Save df_interdiscount as CSV file
file_name = "interdiscount_cleaned.csv"
# Save the DataFrame to CSV in the same directory as the script
df_interdiscount.to_csv(file_name, index=False)

# SAVE CSV
print("-" * 30)
print("------- CSV file saved -------")
print("-" * 30)