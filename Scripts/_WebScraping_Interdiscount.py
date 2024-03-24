# 23.03.2024

# Load libraries, and print selenium version
import selenium
import re
from datetime import datetime
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

print(f'{selenium.__version__=}')

driver = webdriver.Chrome(options=options)
driver2 = webdriver.Chrome(options=options)

# Create an empty pandas DataFrame
df = pd.DataFrame(columns=["id",
                           "brand",
                           "model",
                           "price",
                           "memory",
                           "screen",
                           "camera",
                           "network",
                           "color",
                           "number_reviews",
                           "rating",
                           "delivery_time",
                           "pickup_time",
                           "date"])

# Number of pages to load (there are 15 max in this source)
pages = 15

for i in range(pages):
    url = f"https://www.interdiscount.ch/de/smartphone--c411000?page={i + 1}"
    print(url)
    driver.get(url)

    print(f"--- Driver 1 set to: {url}")

    # Wait for phones to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_3oe9VX')))

    # These class names will change when the CSS file is updated by the developers!
    phones = driver.find_elements(By.CLASS_NAME, '_3oe9VX')

    for phone in phones:
        print(f"Current page: {i+1}")
        price_raw = phone.find_element(By.XPATH,
                                       '//*[@id="TOP_OF_PRODUCTS_LIST"]/div[4]/div[3]/div/a/div[2]/div[1]/div/div').text
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

        # Extracting additional information link
        additional_info_link = phone.find_element(By.CLASS_NAME, 'Q_opE0').get_attribute('href')

        ### Navigate to additional information page ###

        driver2.get(additional_info_link)
        # Wait for elements on the additional information page
        # WebDriverWait(driver2, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="TOP_CONTENT_ANCHOR"]/div/div/div[2]/div[1]/div[2]/small[2]')))

        print(f"--- Driver 2 set to: {additional_info_link}")

        # Extract ID
        try:
            id_element = driver2.find_element(By.XPATH,
                                             '//*[@id="TOP_CONTENT_ANCHOR"]/div/div/div[2]/div[1]/div[2]/small[2]')
            id_match = re.search(r'Artikel-Nr: (\d+)', id_element.text)
            id = id_match.group(1) if id_match else None
        except NoSuchElementException:
            id = None

        # Extract number of reviews
        try:
            number_reviews_element = driver2.find_element(By.CLASS_NAME, '_1top-m').text
            number_reviews_match = re.search(r'\((\d+)\)', number_reviews_element)
            number_reviews = int(number_reviews_match.group(1)) if number_reviews_match else None
        except NoSuchElementException:
            number_reviews = None

        # Extract article rating
        try:
            rating_element = driver2.find_element(By.CLASS_NAME, '_1X48sk')
            rating = float((rating_element.text).split(" ")[0])
        except NoSuchElementException:
            rating = None

        # Extract address delivery time
        try:
            delivery_time_element = driver2.find_element(By.XPATH,
                                                        '//*[@id="TOP_CONTENT_ANCHOR"]/div/div/div[2]/div[2]/div[2]/div/div/div[1]')
            delivery_time = (delivery_time_element.text).split(",\n")[1]
        except IndexError:
            delivery_time = None

        # Extract store pickup time
        try:
            pickup_time_element = driver2.find_element(By.XPATH,
                                                      '//*[@id="TOP_CONTENT_ANCHOR"]/div/div/div[2]/div[2]/div[2]/div/div/div[2]')
            pickup_time = (pickup_time_element.text).split(",\n")[1]
        except IndexError:
            pickup_time = None

        ### Create a dictionary to store phone data ###
        phone_data = {
            "id": id,
            "brand": brand,
            "model": model,
            "price": price,
            "memory": memory,
            "screen": screen,
            "camera": camera,
            "network": network,
            "color": color,
            "number_reviews": number_reviews,
            "rating": rating,
            "delivery_time": delivery_time,
            "pickup_time": pickup_time,
            "date": pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).date()  # Add current date
        }

        # Append phone data to the DataFrame
        df = df._append(phone_data, ignore_index=True)

        ### Print the extracted information ###
        print(f"ID: {id}")
        print(f"Brand: {brand}")
        print(f"Model: {model}")
        print(f"Price: {price}")
        print(f"Memory: {memory}")
        print(f"Screen: {screen}")
        print(f"Camera: {camera}")
        print(f"Network: {network}")
        print(f"Color: {color}")
        print(f"Date: {pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).date()}")
        print(f"Additional link: {additional_info_link}")
        print(f"Nr. reviews: {number_reviews}")
        print(f"Rating: {rating}")
        print(f"Delivery address time: {delivery_time}")
        print(f"Store pickup time: {pickup_time}")
        print("-" * 30)

driver2.close()
driver.close()

print("--- Drivers closed ---")
print("--- Saving CSV ... ---")

# Save df as CSV file
file_name = "interdiscount_scraped.csv"

print("--- CSV file saved ---")

# Save the DataFrame to CSV in the same directory as the script
df.to_csv(file_name, index=False)