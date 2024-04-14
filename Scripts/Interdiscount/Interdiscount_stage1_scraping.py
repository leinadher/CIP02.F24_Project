# 10.04.2024

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
import warnings

# To prevent FutureWarnings from displaying
warnings.simplefilter(action='ignore', category=FutureWarning)

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

        # Extract price:
        try:
            # Find the price element by class name
            price_element = phone.find_element(By.CLASS_NAME, '_3H04_H')
            price_raw = price_element.text

            cleaned_price = re.sub(r'CHF|\.\u2013', '', price_raw).strip()
            # Remove "'" character for thousands separator
            cleaned_price = cleaned_price.replace("'", "")

            # Convert the cleaned price into a float
            price = float(cleaned_price)

        except NoSuchElementException:
            # Handle NoSuchElementException
            price = None

        title_element = phone.find_element(By.CLASS_NAME, 'uIyEJC')

        # Extract title from title element:
        title_raw = title_element.get_attribute("title")

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

        parenthesis = re.search(r"\((.*?)\)[^()]*$", title_raw).group(1)
        parenthesis_list = parenthesis.split(", ")

        memory = None
        camera = None
        network = None
        screen = None
        color_list = []

        for item in parenthesis_list:
            if re.search(r'\d+\s*(?:GB|TB|MB)', item):
                memory = item
            elif re.search(r'\d+\s*MP', item):
                camera = item
            elif re.search(r'\d+G\b', item):
                network = item
            elif re.search(r'^\d+$', item) or re.search(r'^[^a-zA-Z]+$', item):
                # Checks if the string contains only digits or other characters
                screen = item
            else:
                color_list.append(item)

            color = ", ".join(color_list)

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
            "date": pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).date(), # Add current date
            "webpage": additional_info_link
        }

        # Append phone data to the DataFrame
        df = df._append(phone_data, ignore_index=True)

        ### Print the extracted information ###
        # print(parenthesis)
        # print(f"ID: {id}")
        # print(f"Brand: {brand}")
        # print(f"Model: {model}")
        # print(f"Raw: {price_raw}")
        # print(f"Price: {price}")
        # print(f"Memory: {memory}")
        # print(f"Screen: {screen}")
        # print(f"Camera: {camera}")
        # print(f"Network: {network}")
        # print(f"Color: {color}")
        # print(f"Date: {pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).date()}")
        # print(f"Additional link: {additional_info_link}")
        # print(f"Nr. reviews: {number_reviews}")
        # print(f"Rating: {rating}")
        # print(f"Delivery address time: {delivery_time}")
        # print(f"Store pickup time: {pickup_time}")
        print("-" * 30)

driver2.close()
driver.close()

print("--- Drivers clgosed ---")
print("--- Saving CSV ... ---")

########################################################################################################################

# Save df as CSV file
file_name = "data/Interdiscount_stage1.csv"
# Save the DataFrame to CSV in the same directory as the script
df.to_csv(file_name, index=False)

print("-" * 30)
print("----------  STAGE 1 ----------")
print("------- CSV file saved -------")
print("-" * 30)
