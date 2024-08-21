import pandas as pd
import re

df_interdiscount = pd.read_csv("../Data/Interdiscount_stage3_1.csv")

########################################################################################################################

# TRANSFORMATION 01: ADDING A MEMORY VARIABLE WITH ONE ONLY UNIT (GB)

def extract_memory_GB(memory):
    if pd.isna(memory):
        return None

    match = re.search(r'(\d+(\.\d+)?)\s*(MB|GB|TB)', memory, flags=re.IGNORECASE)
    if match:
        value = float(match.group(1))
        unit = match.group(3).lower()
        if unit == 'mb':
            return value / 1000
        elif unit == 'tb':
            return value * 1000
        else:
            return value
    return None

df_interdiscount['memory_GB'] = df_interdiscount['memory'].apply(extract_memory_GB)

# TRANSFORMATION 02: CONVERTING THE 5 STAR RATING TO PERCENTAGE
df_interdiscount['rating100'] = df_interdiscount['rating'] * 20

# TRANSFORMATION 03: SCREEN / PRICE RATIO
# Convert screen inches to float value, in a temporary column
df_interdiscount['screen_price_ratio'] = df_interdiscount['screen'] / df_interdiscount['price']

# TRANSFORMATION 04: REMOVING OLD COLUMNS
df_interdiscount.drop('webpage', axis=1, inplace=True)
df_interdiscount.drop('memory', axis=1, inplace=True)
df_interdiscount.drop('rating', axis=1, inplace=True)

########################################################################################################################

# RENAME AND REMOVE COLUMNS BASED ON GROUP STANDARD

df_interdiscount = df_interdiscount.rename(columns={'camera': 'camera_MP'})
df_interdiscount = df_interdiscount.rename(columns={'screen': 'size'})
df_interdiscount = df_interdiscount.rename(columns={'number_reviews': 'reviews_count'})
df_interdiscount = df_interdiscount.rename(columns={'rating100': 'rating_100'})
df_interdiscount.drop('pickup_time', axis=1, inplace=True)
df_interdiscount['source'] = 'interdiscount'

# Reorder
new_order = ['id',
             'brand',
             'model',
             'memory_GB',
             'camera_MP',
             'size',
             'color',
             'rating_100',
             'reviews_count',
             'price',
             'delivery_time',
             'screen_price_ratio',
             'source',
             'date']
df_interdiscount = df_interdiscount[new_order]

########################################################################################################################

# SAVE CSV

# Save df_interdiscount as CSV file
file_name = "../Data/Interdiscount_stage3_2.csv"
# Save the DataFrame to CSV in the same directory as the script
df_interdiscount.to_csv(file_name, index=False)

print("-" * 30)
print("---------  STAGE 3.2 ---------")
print("------- CSV file saved -------")
print("-" * 30)