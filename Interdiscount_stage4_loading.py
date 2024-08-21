# 15.04.2024

import mariadb
import pandas as pd
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="cip_user",
        password="cip_pw",
        host="localhost",
        port=3306,
        database="CIP"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get cursor
cur = conn.cursor()
print("-" * 30)
print("Cursor:")
print(cur)
print("-" * 30)

########################################################################################################################

# TABLE CREATION
try:
    cur.execute("CREATE TABLE interdiscount (id INT AUTO_INCREMENT PRIMARY KEY, "
                "brand VARCHAR(255), "
                "model VARCHAR(255), "
                "memory_GB INT, "
                "camera_MP FLOAT, "
                "size FLOAT, "
                "color VARCHAR(255), "
                "rating_100 FLOAT, "
                "reviews_count INT, "
                "price FLOAT, "
                "delivery_time INT, "
                "screen_price_ratio FLOAT, "
                "source VARCHAR(255), "
                "date DATE)")

    print("Table created")
    print("-" * 30)
except mariadb.OperationalError:
    print("Skipping table creation, it's already in the database")
    print("-" * 30)
    pass

# TRUNCATE DATA, TO PURGE ALL CONTENTS BEFORE WE EXECUTE
cur.execute("TRUNCATE TABLE interdiscount")

########################################################################################################################

# IMPORT CSV AS PANDAS DATAFRAME
df_interdiscount = pd.read_csv('../Data/Interdiscount_stage3_2.csv')

# DEFINE QUERY
insert_query = """
    INSERT INTO interdiscount 
    (brand, model, memory_GB, camera_MP, size, color, rating_100, reviews_count, price, delivery_time, screen_price_ratio, source, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# ITERATE OVER DATAFRAME AND INSERT ITEMS INTO MARIADB TABLE
for index, row in df_interdiscount.iterrows():
    # Replace NaN values in the current row with None
    row = row.where(pd.notnull(row), None)

    data_tuple = (
        row['brand'], row['model'], row['memory_GB'], row['camera_MP'], row['size'],
        row['color'], row['rating_100'], row['reviews_count'], row['price'],
        row['delivery_time'], row['screen_price_ratio'], row['source'], row['date']
    )
    cur.execute(insert_query, data_tuple)


print("CSV Data loaded successfully")
print("-" * 30)

########################################################################################################################

# TEST
# Select the head (5 items) of the dataset
# We limit the query to 5, then call fetchall()
cur.execute("SELECT * FROM interdiscount LIMIT 5")
rows = cur.fetchall()

for row in rows:
    print(row)
print("-" * 30)

# Also, we compare if the number of items on the dataframe is the same as on the table
cur.execute("SELECT COUNT(*) FROM interdiscount")
result = cur.fetchone()
count = result[0]
print("Number of items on CSV:  ", len(df_interdiscount))
print("Number of items on table:", count)
print("-" * 30)

########################################################################################################################

# CLOSE CONNECTION
print("Closing connection...")
print("-" * 30)
conn.commit()
cur.close()
conn.close()
print("Connection closed")
print("-" * 30)