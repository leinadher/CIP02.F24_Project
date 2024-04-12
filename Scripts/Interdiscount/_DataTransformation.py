import pandas as pd
import re

df_interdiscount = pd.read_csv("interdiscount_cleaned.csv")

print(df_interdiscount.head())

# TRANSFORMATION 01: ADDING A MEMORY VARIABLE WITH ONE ONLY UNIT (GB):
# Define a function to extract and convert memory values
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
df_interdiscount['screen_temp'] = df_interdiscount['screen'].apply(lambda x: float(x.rstrip('"')))
df_interdiscount['screen_price_ratio'] = df_interdiscount['screen_temp'] / df_interdiscount['price']
df_interdiscount.drop(columns=['screen_temp'], inplace=True)

# TRANSFORMATION 04: REMOVING OLD COLUMNS
df_interdiscount.drop('webpage', axis=1, inplace=True)
df_interdiscount.drop('memory', axis=1, inplace=True)
df_interdiscount.drop('rating', axis=1, inplace=True)

# Save df_interdiscount as CSV file
file_name = "interdiscount_transformed.csv"
# Save the DataFrame to CSV in the same directory as the script
df_interdiscount.to_csv(file_name, index=False)

# SAVE CSV
print("-" * 30)
print("------- CSV file saved -------")
print("-" * 30)