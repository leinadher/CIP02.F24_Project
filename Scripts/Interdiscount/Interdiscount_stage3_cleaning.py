# 24.03.2024

import re
import pandas as pd
import warnings
from _DeliveryPickupTime import convert_delivery_time, convert_pickup_time
from _TranslateColors import translate_and_lowercase, corrector

# To prevent FutureWarnings from displaying
warnings.simplefilter(action='ignore', category=FutureWarning)

df_interdiscount = pd.read_csv("data/Interdiscount_stage1.csv")

########################################################################################################################

# ID AS STRING
df_interdiscount['id'] = pd.to_numeric(df_interdiscount['id'], errors='coerce').astype(pd.Int64Dtype())
df_interdiscount['id'] = df_interdiscount['id'].astype(str)

# BRAND LOWERCASE
df_interdiscount['brand'] = df_interdiscount['brand'].apply(lambda x: x.lower() if pd.notna(x) else None)

# MODEL LOWERCASE
df_interdiscount['model'] = df_interdiscount['model'].apply(lambda x: x.lower() if pd.notna(x) else None)

# PRICE AS FLOAT
df_interdiscount['price'].fillna(df_interdiscount['price'].mean(), inplace=True)

# SCREEN AS FLOAT
df_interdiscount['screen'] = df_interdiscount['screen'].apply(lambda x: float(x.strip('"')) if x is not None else None)

# CAMERA AS FLOAT
df_interdiscount['camera'] = df_interdiscount['camera'].apply(lambda x: float(x.strip(' MP')) if pd.notna(x) else None)

# COLOR TRANSLATE DE-EN AND LOWERCASE
df_interdiscount['color'] = df_interdiscount['color'].apply(translate_and_lowercase)
df_interdiscount['color'] = df_interdiscount['color'].apply(corrector)

# RATING AS FLOAT
df_interdiscount['rating'] = df_interdiscount['rating'].astype(float)

# DELIVERY TIME AS INTEGER
df_interdiscount['delivery_time'] = [convert_delivery_time(i) for i in df_interdiscount['delivery_time']]
df_interdiscount['delivery_time'] = df_interdiscount['delivery_time'].astype(pd.Int64Dtype())

# PICKUP TIME AS INTEGER
df_interdiscount['pickup_time'] = [convert_pickup_time(i) for i in df_interdiscount['pickup_time']]
df_interdiscount['delivery_time'] = df_interdiscount['pickup_time'].astype(pd.Int64Dtype())

########################################################################################################################

# FIXING "NOTHING" BRAND DATA
# Models of the "NOTHING" brand contain parenthesis
# Because previous regex was looking for a parenthesis structure in the title, all other fields were filed in wrongly
# The following code repairs these rows by generating the data from different sources

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

########################################################################################################################

# Save df_interdiscount as CSV file
file_name = "data/Interdiscount_stage3_1.csv"
# Save the DataFrame to CSV in the same directory as the script
df_interdiscount.to_csv(file_name, index=False)

# SAVE CSV
print("-" * 30)
print("---------  STAGE 3.1 ---------")
print("------- CSV file saved -------")
print("-" * 30)