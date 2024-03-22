# 13.03.2024

# pip install selenium
# Load libraries, and print selenium version
import selenium
import time
import re
from datetime import datetime
import pandas as pd
print(f'{selenium.__version__=}')

########################################################################################################################

from selenium.webdriver.common.by import By
from selenium import webdriver
driver = webdriver.Chrome()

# Create an empty pandas DataFrame
df = pd.DataFrame(columns=["brand", "model", "price", "memory", "screen", "camera", "network", "color", "date"])

for i in range(1):
    url = f"https://www.interdiscount.ch/de/search?search=Smartphone&page={i + 1}"
    print(url)
    driver.get(url)

    # Add a delay to give the page time to load
    time.sleep(2)

    phones = driver.find_elements(By.CLASS_NAME, '_3UBePl._1Tqbve._1Z-HSp._1__h-Q._368eQg')

    for phone in phones:
        price_raw = phone.find_element(By.XPATH, './/div[@class="krweWr _19DrBd"]/div').text
        title_element = phone.find_element(By.CLASS_NAME, 'uIyEJC')

        # Extract title from title element:
        title_raw = title_element.get_attribute("title")

        # Extract numerical value from price string
        price_match = re.search(r'(\d[\'\d]*)', price_raw)
        if price_match:
            # Remove the thousands separator
            price = float(price_match.group().replace("'", ""))
        else:
            price = None

        # Extract brand
        brand_match = re.match(r'^(\w+)', title_raw)
        if brand_match:
            brand = brand_match.group(1)
        else:
            continue  # Skip if brand is not found

        # Extract model
        model_match = re.search(rf'{re.escape(brand)}\s+(.+?)\s*\(', title_raw)
        if model_match:
            model = model_match.group(1)
        else:
            continue  # Skip if model is not found

        # Extract memory
        memory_match = re.search(r'(\d+\s*GB)', title_raw)
        memory = memory_match.group(1) if memory_match else None

        # Extract screen
        screen_match = re.search(r'(\d+(\.\d+)?")', title_raw)
        screen = screen_match.group(1) if screen_match else None

        # Extract camera
        camera_match = re.search(r'(\d+\s*MP)', title_raw)
        camera = camera_match.group(1) if camera_match else None

        # Extract network
        network_match = re.search(r'\b(4G|5G)\b', title_raw)
        network = network_match.group(1) if network_match else None

        # Extract color
        color_match = re.search(r',\s*([^,()]+)', title_raw)
        color = color_match.group(1) if color_match else None

        # Create a dictionary to store phone data
        phone_data = {
            "brand": brand,
            "model": model,
            "price": price,
            "memory": memory,
            "screen": screen,
            "camera": camera,
            "network": network,
            "color": color,
            "date": pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))  # Add current date
        }

        # Append phone data to the DataFrame
        df = df._append(phone_data, ignore_index=True)

        # Print or use the extracted information
        print(f"Brand: {brand}")
        print(f"Model: {model}")
        print(f"Price: {price}")
        print(f"Memory: {memory}")
        print(f"Screen: {screen}")
        print(f"Camera: {camera}")
        print(f"Network: {network}")
        print(f"Color: {color}")
        print(f"Date: {pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))}")
        print("-" * 30)

